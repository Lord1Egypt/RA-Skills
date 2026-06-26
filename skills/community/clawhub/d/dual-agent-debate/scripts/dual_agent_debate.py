#!/usr/bin/env python3
import argparse
import json
import math
import os
import random
import subprocess
import time
from datetime import datetime, timezone
from typing import Optional
from urllib import error, request


def _sleep_backoff(attempt: int, base: float = 0.8):
    time.sleep(base * (2 ** attempt) + random.uniform(0, 0.25))


def post_json(url: str, payload: dict, headers: Optional[dict] = None, timeout: int = 60):
    body = json.dumps(payload).encode("utf-8")
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if headers:
        h.update(headers)
    req = request.Request(url, data=body, headers=h, method="POST")
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def safe_sql_str(value: str) -> str:
    # dollar-quote with collision-safe tag
    tag = "q"
    while f"${tag}$" in value:
        tag += "q"
    return f"${tag}${value}${tag}$"


def mcp_call(tool_name: str, arguments: dict, retries: int = 2):
    url = os.environ.get("OPENBRAIN_MCP_URL", "http://127.0.0.1:54321/mcp")
    token = os.environ.get("OPENBRAIN_MCP_TOKEN", "")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }

    for attempt in range(retries + 1):
        try:
            out = post_json(url, payload, headers=headers, timeout=60)
            if "error" in out:
                msg = str(out["error"])
                if attempt < retries and any(k in msg.lower() for k in ["timeout", "429", "rate", "tempor"]):
                    _sleep_backoff(attempt)
                    continue
                return {"ok": False, "error": out["error"]}
            return {"ok": True, "result": out.get("result")}
        except Exception as e:
            if attempt < retries:
                _sleep_backoff(attempt)
                continue
            return {"ok": False, "error": str(e)}


def cli_agent_chat(messages: list[dict]) -> str:
    prompt = "\n\n".join([f"{m.get('role','user').upper()}: {m.get('content','')}" for m in messages])
    cmd = ["openclaw", "agent", "--json", "--agent", "main", "--thinking", "off", "--message", prompt]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    data = None
    try:
        data = json.loads(out)
    except Exception:
        i = out.rfind("{")
        while i != -1:
            try:
                data = json.loads(out[i:])
                break
            except Exception:
                i = out.rfind("{", 0, i)
    if not isinstance(data, dict):
        raise RuntimeError("Could not parse openclaw agent JSON output")
    payloads = data.get("payloads", [])
    if not payloads:
        raise RuntimeError("No payloads from openclaw agent")
    return (payloads[0].get("text") or "").strip()


def openai_chat(messages: list[dict], model: str, retries: int = 2) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return cli_agent_chat(messages)

    payload = {"model": model, "messages": messages, "temperature": 0.2}
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(retries + 1):
        try:
            out = post_json("https://api.openai.com/v1/chat/completions", payload, headers=headers, timeout=90)
            return out["choices"][0]["message"]["content"].strip()
        except Exception:
            if attempt < retries:
                _sleep_backoff(attempt)
                continue
            raise


def openai_embedding(text: str, model: str = "text-embedding-3-small", retries: int = 2) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        # lexical fallback vector: hashed token counts (128 dims)
        vec = [0.0] * 128
        for tok in text.lower().split():
            vec[hash(tok) % 128] += 1.0
        return vec

    payload = {"model": model, "input": text[:8000]}
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(retries + 1):
        try:
            out = post_json("https://api.openai.com/v1/embeddings", payload, headers=headers, timeout=90)
            return out["data"][0]["embedding"]
        except Exception:
            if attempt < retries:
                _sleep_backoff(attempt)
                continue
            raise


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def extract_text(mcp_result) -> str:
    if isinstance(mcp_result, str):
        return mcp_result
    if isinstance(mcp_result, dict):
        if "content" in mcp_result and isinstance(mcp_result["content"], str):
            return mcp_result["content"]
        if "content" in mcp_result and isinstance(mcp_result["content"], list):
            return "\n".join(str(x.get("text", x)) if isinstance(x, dict) else str(x) for x in mcp_result["content"])
        return json.dumps(mcp_result)[:12000]
    if isinstance(mcp_result, list):
        return "\n".join(extract_text(x) for x in mcp_result)[:12000]
    return str(mcp_result)


def sql_query(sql_tool: str, query: str) -> dict:
    return mcp_call(sql_tool, {"query": query})


def detect_columns(sql_tool: str, table_name: str) -> set[str]:
    q = f"""
    select column_name
    from information_schema.columns
    where table_schema = 'public' and table_name = {safe_sql_str(table_name)};
    """
    r = sql_query(sql_tool, q)
    if not r.get("ok"):
        return set()
    txt = extract_text(r.get("result"))
    cols = set()
    for token in txt.replace('"', "").replace("'", "").split():
        if token.isidentifier():
            cols.add(token.lower())
    # fallback known columns if parser misses
    for name in ["content", "created_at", "key", "category", "importance", "source", "metadata"]:
        if name in txt.lower():
            cols.add(name)
    return cols


def fetch_candidate_thoughts(sql_tool: str, query: str, limit: int = 30) -> list[str]:
    q = f"""
    select content
    from public.thoughts
    where content is not null and length(content) > 0
    order by created_at desc
    limit {int(limit)};
    """
    r = sql_query(sql_tool, q)
    if not r.get("ok"):
        return []
    txt = extract_text(r.get("result"))
    # lenient parser: split by line, keep non-empty payload-like lines
    lines = [ln.strip(" -\t") for ln in txt.splitlines() if ln.strip()]
    candidates = [ln for ln in lines if len(ln) > 20]
    return candidates[:limit]


def semantic_select_thoughts(query: str, candidates: list[str], top_k: int = 6) -> str:
    if not candidates:
        return ""
    q_emb = openai_embedding(query)
    scored = []
    for c in candidates:
        try:
            sim = cosine(q_emb, openai_embedding(c[:2000]))
        except Exception:
            sim = 0.0
        scored.append((sim, c))
    scored.sort(reverse=True, key=lambda x: x[0])
    picked = [t for _, t in scored[:top_k]]
    return "\n\n---\n\n".join(picked)


def main():
    p = argparse.ArgumentParser(description="DualAgentDebate: ChatGPT + Open Brain MCP debate loop")
    p.add_argument("--query", required=True, help="User query to debate")
    p.add_argument("--thoughts", default="", help="Optional explicit thoughts text")
    p.add_argument("--rounds", type=int, default=3)
    p.add_argument("--agreement-threshold", type=float, default=0.90)
    p.add_argument("--model", default=os.environ.get("DEBATE_MODEL", "gpt-4o-mini"))
    args = p.parse_args()

    context_tool = os.environ.get("OPENBRAIN_CONTEXT_TOOL", "search_docs")
    sql_tool = os.environ.get("OPENBRAIN_SQL_TOOL", "execute_sql")

    # Context retrieval
    context = ""
    q_gql = args.query.replace('\\', '\\\\').replace('"', '\\"')
    gql = (
        'query { searchDocs(query: "' + q_gql + '", limit: 5) '
        '{ nodes { ... on Guide { title href content } '
        '... on TroubleshootingGuide { title href content } '
        '... on CLICommandReference { title href content } } } }'
    )
    c = mcp_call(context_tool, {"graphql_query": gql})
    if c.get("ok"):
        context = extract_text(c.get("result"))[:8000]

    # Thought retrieval with semantic rerank
    thoughts = args.thoughts.strip()
    if not thoughts:
        candidates = fetch_candidate_thoughts(sql_tool, args.query, limit=25)
        thoughts = semantic_select_thoughts(args.query, candidates, top_k=6)

    if not thoughts:
        thoughts = "No prior thoughts found in Open Brain."

    rounds = []
    final_similarity = 0.0
    agreed = False
    run_id = f"dab-{int(time.time())}"

    system = (
        "You are Debate Agent A (ChatGPT). Use supplied Open Brain context. "
        "Provide concise reasoning, then a final stance."
    )

    prior = ""
    for i in range(1, max(1, args.rounds) + 1):
        user_prompt = (
            f"Round {i}. Query: {args.query}\n\n"
            f"Open Brain Context:\n{context[:6000]}\n\n"
            f"My thoughts (Agent B):\n{thoughts[:6000]}\n\n"
            f"Prior round summary:\n{prior}\n\n"
            "Respond with:\n"
            "1) Claim\n2) Evidence\n3) Counterpoint to my thoughts\n4) Revised stance"
        )

        reply = openai_chat([
            {"role": "system", "content": system},
            {"role": "user", "content": user_prompt},
        ], args.model)

        emb_reply = openai_embedding(reply)
        emb_thoughts = openai_embedding(thoughts)
        sim = cosine(emb_reply, emb_thoughts)
        final_similarity = sim
        prior = f"Similarity to my thoughts: {sim:.3f}. Key points: {reply[:1200]}"

        rounds.append({"round": i, "similarity": round(sim, 4), "reply": reply[:6000]})
        if sim >= args.agreement_threshold:
            agreed = True
            break

    outcome = {
        "run_id": run_id,
        "query": args.query,
        "agreed": agreed,
        "final_similarity": round(final_similarity, 4),
        "rounds_executed": len(rounds),
        "rounds": rounds,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
    }

    # Storage with schema guardrails
    mem_cols = detect_columns(sql_tool, "memories")
    outcome_json = json.dumps(outcome, ensure_ascii=False)
    if len(outcome_json) > 12000:
        outcome_json = outcome_json[:12000] + "...<truncated>"

    key = f"dual-agent-debate:{int(time.time())}"
    values = {
        "key": safe_sql_str(key),
        "content": safe_sql_str(outcome_json),
        "category": safe_sql_str("decision"),
        "importance": "2",
        "source": safe_sql_str("DualAgentDebate"),
        "metadata": safe_sql_str(json.dumps({"run_id": run_id, "query": args.query}, ensure_ascii=False)),
    }

    ordered_cols = [c for c in ["key", "content", "category", "importance", "source", "metadata"] if c in mem_cols]
    if not ordered_cols:
        ordered_cols = ["key", "content"]

    col_sql = ", ".join(ordered_cols)
    val_sql = ", ".join(values[c] for c in ordered_cols)
    insert_sql = f"insert into public.memories ({col_sql}) values ({val_sql}) returning *;"

    saved = sql_query(sql_tool, insert_sql)
    saved_txt = (extract_text(saved.get("result")) if isinstance(saved, dict) else str(saved))
    saved_l = saved_txt.lower()
    missing_memories = ("public.memories" in saved_l and "does not exist" in saved_l)
    if (not saved.get("ok")) or missing_memories:
        create_sql = """
        create table if not exists public.memories (
          id bigserial primary key,
          key text unique,
          content text,
          category text,
          importance integer,
          source text,
          metadata jsonb,
          created_at timestamptz default now()
        );
        """
        _ = sql_query(sql_tool, create_sql)
        saved = sql_query(sql_tool, insert_sql)

    print(json.dumps({
        "outcome": outcome,
        "store": saved,
        "store_tool": sql_tool,
        "context_tool": context_tool,
        "notes": [
            "thought retrieval: semantic rerank over recent public.thoughts content",
            "storage: column-aware insert into public.memories",
        ],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
