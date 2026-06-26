#!/usr/bin/env python3
import argparse
import json
import os
import random
import subprocess
import time
from datetime import datetime, timezone
from typing import Optional
from urllib import request


def sleep_backoff(i: int):
    time.sleep(0.8 * (2 ** i) + random.uniform(0, 0.2))


def post_json(url: str, payload: dict, headers: Optional[dict] = None, timeout: int = 60):
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if headers:
        h.update(headers)
    req = request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=h, method="POST")
    with request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def mcp_call(tool: str, arguments: dict, retries: int = 2):
    url = os.environ.get("OPENBRAIN_MCP_URL", "http://127.0.0.1:54321/mcp")
    tok = os.environ.get("OPENBRAIN_MCP_TOKEN", "")
    headers = {"Authorization": f"Bearer {tok}"} if tok else {}
    payload = {"jsonrpc": "2.0", "id": int(time.time() * 1000), "method": "tools/call", "params": {"name": tool, "arguments": arguments}}
    for i in range(retries + 1):
        try:
            out = post_json(url, payload, headers=headers, timeout=60)
            if "error" in out:
                if i < retries:
                    sleep_backoff(i)
                    continue
                return {"ok": False, "error": out["error"]}
            return {"ok": True, "result": out.get("result")}
        except Exception as e:
            if i < retries:
                sleep_backoff(i)
                continue
            return {"ok": False, "error": str(e)}


def extract_text(x) -> str:
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        if isinstance(x.get("content"), str):
            return x["content"]
        if isinstance(x.get("content"), list):
            return "\n".join(str(i.get("text", i)) if isinstance(i, dict) else str(i) for i in x["content"])
        return json.dumps(x)[:12000]
    if isinstance(x, list):
        return "\n".join(extract_text(i) for i in x)[:12000]
    return str(x)


def safe_sql_str(v: str) -> str:
    tag = "q"
    while f"${tag}$" in v:
        tag += "q"
    return f"${tag}${v}${tag}$"


def parse_openclaw_json(out: str) -> dict:
    try:
        return json.loads(out)
    except Exception:
        i = out.rfind("{")
        while i != -1:
            try:
                return json.loads(out[i:])
            except Exception:
                i = out.rfind("{", 0, i)
    raise RuntimeError("Could not parse openclaw agent output")


def openclaw_agent_turn(system_role: str, prompt: str) -> str:
    msg = f"SYSTEM ROLE:\n{system_role}\n\nTASK:\n{prompt}"
    cmd = ["openclaw", "agent", "--json", "--agent", "main", "--thinking", "off", "--message", msg]
    out = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    data = parse_openclaw_json(out)
    payloads = data.get("payloads", [])
    if not payloads:
        raise RuntimeError("No payload text returned")
    return (payloads[0].get("text") or "").strip()


def maybe_openai_turn(system_role: str, prompt: str) -> str:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return openclaw_agent_turn(system_role, prompt)
    payload = {
        "model": os.environ.get("SOLVER_SECOND_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    headers = {"Authorization": f"Bearer {key}"}
    out = post_json("https://api.openai.com/v1/chat/completions", payload, headers=headers, timeout=90)
    return out["choices"][0]["message"]["content"].strip()


def ensure_memories_table(sql_tool: str):
    q = """
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
    _ = mcp_call(sql_tool, {"query": q})


def main():
    ap = argparse.ArgumentParser(description="DualAgentSolver: 2-agent collaborative solver with one OpenClaw agent")
    ap.add_argument("--query", required=True)
    ap.add_argument("--rounds", type=int, default=3)
    args = ap.parse_args()

    sql_tool = os.environ.get("OPENBRAIN_SQL_TOOL", "execute_sql")
    docs_tool = os.environ.get("OPENBRAIN_CONTEXT_TOOL", "search_docs")

    # Optional context pull
    q = args.query.replace('\\', '\\\\').replace('"', '\\"')
    gql = 'query { searchDocs(query: "' + q + '", limit: 4) { nodes { ... on Guide { title href content } ... on CLICommandReference { title href content } } } }'
    ctx = mcp_call(docs_tool, {"graphql_query": gql})
    context = extract_text(ctx.get("result"))[:6000] if ctx.get("ok") else ""

    solver_role = (
        "You are Agent A (OpenClaw primary solver). Produce practical implementation plans with clear steps, tradeoffs, and rollback strategy."
    )
    critic_role = (
        "You are Agent B (adversarial reviewer). Find hidden risks, edge cases, missing assumptions, and force stronger plans."
    )

    a_plan = ""
    b_crit = ""
    rounds = []

    for i in range(1, max(1, args.rounds) + 1):
        a_prompt = (
            f"Round {i}. Problem: {args.query}\n\n"
            f"Context:\n{context}\n\n"
            f"Previous critique:\n{b_crit}\n\n"
            "Output:\n1) Proposed solution\n2) Steps\n3) Risks\n4) Rollback"
        )
        a_plan = openclaw_agent_turn(solver_role, a_prompt)

        b_prompt = (
            f"Round {i}. Evaluate this plan strictly:\n\n{a_plan}\n\n"
            "Output:\n1) Critical flaws\n2) Missing assumptions\n3) Better alternative\n4) Acceptance conditions"
        )
        b_crit = maybe_openai_turn(critic_role, b_prompt)

        rounds.append({"round": i, "solver": a_plan[:5000], "critic": b_crit[:5000]})

    final_prompt = (
        f"Problem: {args.query}\n\n"
        f"Latest solver plan:\n{a_plan}\n\n"
        f"Latest critic review:\n{b_crit}\n\n"
        "Produce ONE merged final answer:\n"
        "- Decision\n- Why\n- Step-by-step execution plan\n- Risk mitigations\n- Rollback plan\n- 3 immediate next actions"
    )
    final_solution = openclaw_agent_turn(solver_role, final_prompt)

    outcome = {
        "run_id": f"das-{int(time.time())}",
        "query": args.query,
        "rounds_executed": len(rounds),
        "rounds": rounds,
        "final_solution": final_solution,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    ensure_memories_table(sql_tool)
    key = f"dual-agent-solver:{int(time.time())}"
    ins = (
        "insert into public.memories (key, content, category, importance, source, metadata) values ("
        f"{safe_sql_str(key)}, {safe_sql_str(json.dumps(outcome, ensure_ascii=False)[:14000])}, "
        f"{safe_sql_str('solution')}, 3, {safe_sql_str('DualAgentSolver')}, {safe_sql_str(json.dumps({'query': args.query, 'run_id': outcome['run_id']}, ensure_ascii=False))}::jsonb"
        ") returning key, created_at;"
    )
    saved = mcp_call(sql_tool, {"query": ins})

    print(json.dumps({"outcome": outcome, "store": saved, "memory_key": key}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
