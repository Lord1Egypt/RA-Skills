#!/usr/bin/env python3
"""
multihop_search — Multi-hop reasoning search over QMD-indexed markdown.
Chains search queries to find complex answers across workspace knowledge.

Usage:
    multihop_search "question" [--max-hops 4] [--qmd] [--debug] [--json]
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import argparse, json, subprocess, time, math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config, call_llm_json, call_llm, embed, cosine_sim


def qmd_search(query: str, limit: int = 10, debug: bool = False) -> list[dict]:
    """Search via QMD CLI (JSON mode)."""
    try:
        result = subprocess.run(
            ["qmd", "search", query, "--limit", str(limit), "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            if debug:
                print(f"  QMD error: {result.stderr[:200]}", file=sys.stderr)
            return []
        
        raw = json.loads(result.stdout)
        results = []
        for item in raw:
            filepath = item.get("file", "").replace("qmd://workspace/", "")
            results.append({
                "filepath": filepath,
                "line": 1,
                "text": item.get("snippet", item.get("title", "")),
                "score": item.get("score", 0),
                "title": item.get("title", "")
            })
        return results
    except (json.JSONDecodeError, FileNotFoundError) as e:
        if debug:
            print(f"  QMD exception: {e}", file=sys.stderr)
        return []


def embed_search(query: str, cfg: dict, limit: int = 10, debug: bool = False) -> list[dict]:
    """Search workspace using vector embeddings (more accurate than BM25 for French)."""
    ws = cfg["paths"]["workspace"]
    cache_path = os.path.join(ws, cfg["paths"].get("embedCache", ".cache/embed-chunks.json"))
    
    if not os.path.exists(cache_path):
        if debug:
            print(f"  Embed cache not found: {cache_path}", file=sys.stderr)
        return []
    
    try:
        with open(cache_path) as f:
            cache = json.load(f)
    except Exception as e:
        if debug:
            print(f"  Embed cache load error: {e}", file=sys.stderr)
        return []
    
    chunks = cache.get("chunks", [])
    if not chunks:
        return []
    
    # Embed query
    query_vec = embed([query], cfg, debug)
    if not query_vec or not query_vec[0]:
        if debug:
            print("  Query embedding failed", file=sys.stderr)
        return []
    
    qv = query_vec[0]
    
    # Score all chunks
    scored = []
    for chunk in chunks:
        vec = chunk.get("embedding") or chunk.get("vector")
        if not vec:
            continue
        sim = cosine_sim(qv, vec)
        scored.append((sim, chunk))
    
    scored.sort(key=lambda x: -x[0])
    
    results = []
    for sim, chunk in scored[:limit]:
        results.append({
            "filepath": chunk.get("file", chunk.get("filepath", "?")),
            "line": chunk.get("line", 1),
            "text": chunk.get("text", chunk.get("content", ""))[:500],
            "score": round(sim, 4),
            "source": "embed"
        })
    
    if debug:
        print(f"  Embed search: {len(results)} results (top score: {results[0]['score'] if results else 0})", file=sys.stderr)
    
    return results


def load_knowledge_graph(cfg: dict) -> dict:
    """Load knowledge graph if available."""
    ws = cfg["paths"]["workspace"]
    graph_path = os.path.join(ws, cfg["paths"]["knowledgeGraph"])
    try:
        with open(graph_path) as f:
            return json.load(f)
    except Exception:
        return {}


def enrich_with_graph(query: str, results: list[dict], graph: dict, debug: bool = False) -> list[dict]:
    """Add related files from knowledge graph."""
    if not graph:
        return results
    
    entities = graph.get("entities", {})
    query_lower = query.lower()
    related_files = set()
    
    # Support both dict format {"Name": {...}} and list format [{"name": "..."}]
    if isinstance(entities, dict):
        items = [(name, data) for name, data in entities.items()]
    elif isinstance(entities, list):
        items = [(e.get("name", ""), e) for e in entities if isinstance(e, dict)]
    else:
        return results
    
    for name, data in items:
        if name.lower() in query_lower or query_lower in name.lower():
            # Get related files from mentions/relations
            for f in data.get("mentions", []):
                related_files.add(f)
            for rel in data.get("relations", []):
                if isinstance(rel, dict):
                    target = rel.get("target", "")
                    if target:
                        related_files.add(target)
                elif isinstance(rel, str):
                    related_files.add(rel)
            if debug:
                print(f"  Graph: '{name}' → {len(related_files)} files", file=sys.stderr)
    
    # Score files by relevance: prioritize query keywords in filename
    query_words = set(query_lower.split())
    scored = []
    for f in related_files:
        f_lower = f.lower()
        # Score: keyword matches in path + bonus for memory/ and bugs/
        score = sum(1 for w in query_words if w in f_lower)
        if "memory/" in f_lower or "bugs/" in f_lower:
            score += 2
        if "agents/" in f_lower:
            score += 1
        scored.append((score, f))
    
    scored.sort(key=lambda x: -x[0])
    
    existing = {r.get("filepath", "") for r in results}
    graph_added = 0
    for score, f in scored[:8]:  # Top 8 most relevant
        if f not in existing:
            results.append({"filepath": f, "line": 1, "text": f"[graph] Related: {f}", "source": "graph", "score": score})
            graph_added += 1
    
    if debug:
        print(f"  Graph enrichment: +{graph_added} files (from {len(related_files)} candidates)", file=sys.stderr)
    
    return results


def synthesize(question: str, results: list[dict], cfg: dict, debug: bool = False) -> dict:
    """Ask LLM to synthesize an answer from search results."""
    if not results:
        return {"action": "answer", "answer": "No results found.", "confidence": 0.0}
    
    context = "\n".join([
        f"[{r.get('filepath', '?')}:{r.get('line', '?')}] {r.get('text', '')[:500]}"
        for r in results[:15]
    ])
    
    prompt = f"""Question: {question}

Context from workspace files:
{context}

Respond in JSON:
{{"action": "answer"|"refine", "answer": "your answer (if action=answer)", "confidence": 0.0-1.0, "next_query": "refined query (if action=refine)", "sources": ["file1.md", "file2.md"]}}

Rules:
- If you can answer confidently → action=answer
- If you need more info → action=refine with a better search query
- confidence: 0.0-1.0 based on how well the context answers the question
- Always cite sources"""
    
    result = call_llm_json(prompt, cfg, debug)
    if result:
        return result
    
    # Fallback: raw text answer
    text = call_llm(prompt, cfg, debug)
    return {"action": "answer", "answer": text or "LLM failed", "confidence": 0.2}


def multihop(question: str, max_hops: int = 4, use_qmd: bool = True,
             use_embed: bool = False, cfg: dict | None = None, debug: bool = False) -> dict:
    """Execute multi-hop search."""
    if cfg is None:
        cfg = load_config(script="multihop")
    
    graph = load_knowledge_graph(cfg)
    all_results = []
    hops_log = []
    query = question
    
    for hop in range(1, max_hops + 1):
        t0 = time.time()
        
        if debug:
            print(f"\n--- Hop {hop}/{max_hops} ---", file=sys.stderr)
            print(f"  Query: {query}", file=sys.stderr)
        
        # Search — combine QMD + embeddings for better recall
        results = qmd_search(query, limit=cfg["qmd"]["defaultLimit"], debug=debug)
        
        if use_embed:
            embed_results = embed_search(query, cfg, limit=cfg["qmd"]["defaultLimit"], debug=debug)
            # Merge: deduplicate by filepath
            existing = {r.get("filepath", "") for r in results}
            for er in embed_results:
                if er.get("filepath", "") not in existing:
                    results.append(er)
                    existing.add(er["filepath"])
        
        # Enrich with knowledge graph
        results = enrich_with_graph(query, results, graph, debug)
        
        elapsed = time.time() - t0
        if debug:
            print(f"  Results: {len(results)} ({elapsed:.1f}s)", file=sys.stderr)
        
        hops_log.append({"hop": hop, "query": query, "results": len(results), "time": elapsed})
        
        # Deduplicate
        seen = {r.get("filepath", "") + str(r.get("line", "")) for r in all_results}
        for r in results:
            key = r.get("filepath", "") + str(r.get("line", ""))
            if key not in seen:
                all_results.append(r)
                seen.add(key)
        
        # Synthesize
        synthesis = synthesize(question, all_results, cfg, debug)
        
        if synthesis.get("action") == "answer" and synthesis.get("confidence", 0) >= cfg["search"]["confidenceThreshold"]:
            return {
                "answer": synthesis.get("answer", ""),
                "confidence": synthesis.get("confidence", 0),
                "hops": hop,
                "total_results": len(all_results),
                "sources": synthesis.get("sources", []),
                "hops_log": hops_log
            }
        
        # Refine query for next hop
        if synthesis.get("next_query"):
            query = synthesis["next_query"]
        else:
            break
    
    # Forced synthesis
    final = synthesize(question, all_results, cfg, debug)
    return {
        "answer": final.get("answer", "No conclusive answer found."),
        "confidence": final.get("confidence", 0.2),
        "hops": len(hops_log),
        "total_results": len(all_results),
        "sources": final.get("sources", []),
        "hops_log": hops_log,
        "forced": True
    }


def main():
    parser = argparse.ArgumentParser(description="Multi-hop reasoning search")
    parser.add_argument("question", help="Question to search for")
    parser.add_argument("--max-hops", type=int, default=4)
    parser.add_argument("--qmd", action="store_true", help="Use QMD search")
    parser.add_argument("--embed", action="store_true", help="Also use vector embeddings (better recall)")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--preset", help="Config preset (ollama, openai)")
    args = parser.parse_args()
    
    cfg = load_config(preset=args.preset, script="multihop")
    result = multihop(args.question, max_hops=args.max_hops, use_qmd=args.qmd,
                      use_embed=args.embed, cfg=cfg, debug=args.debug)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        icon = "✅" if result["confidence"] >= 0.7 else "💡" if result["confidence"] >= 0.4 else "⚠"
        print(f"\n{icon} {result['answer']}")
        print(f"\n📊 Confidence: {int(result['confidence']*100)}% | Hops: {result['hops']} | Results: {result['total_results']}")
        if result.get("sources"):
            print(f"📎 Sources: {', '.join(result['sources'][:5])}")
        if result.get("forced"):
            print("⚠ Forced synthesis (insufficient confidence)")


if __name__ == "__main__":
    main()
