#!/usr/bin/env python3
"""
unified_recall — Unified memory recall pipeline.
Fan-out vers 4 sources, merge, scoring multi-signal, rerank LLM.

Architecture:
  Question → [agentMemory, embeddings, QMD, graph] → merge → score → rerank → answer

Usage:
    unified_recall.py "question" [--top 8] [--rerank] [--debug] [--json]
    unified_recall.py "question" --no-llm    # scoring only, no synthesis
"""
from __future__ import annotations
import os, sys
# Cross-platform PATH setup
if sys.platform == "darwin":
    os.environ["PATH"] = "/opt/homebrew/bin:" + os.environ.get("HOME", "") + "/.bun/bin:" + os.environ.get("PATH", "")

import argparse, json, math, re, subprocess, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from llm_client import load_config, call_llm_json, call_llm, embed, cosine_sim
from fact_store import FactStore


# === Source weights ===
SOURCE_TRUST = {
    "convex": 1.0,      # agentMemory / local facts = source of truth
    "embed": 0.8,       # semantic similarity
    "qmd": 0.6,         # BM25 text match
    "graph": 0.5,       # entity relations
}

SCORE_WEIGHTS = {
    "semantic": 0.30,    # w1: embed cosine similarity
    "bm25": 0.15,        # w2: QMD text score
    "recency": 0.20,     # w3: temporal decay
    "access": 0.10,      # w4: access frequency (agentMemory)
    "trust": 0.15,       # w5: source trust level
    "graph": 0.10,       # w6: graph centrality
}

# =====================================================================
# Source 1: agentMemory (Convex) or local JSON (auto-detected)
# =====================================================================
_fact_store_instance = None

def _get_fact_store(cfg: dict = None) -> FactStore:
    global _fact_store_instance
    if _fact_store_instance is None:
        _fact_store_instance = FactStore(cfg)
    return _fact_store_instance


def search_convex(query: str, debug: bool = False, cfg: dict = None) -> list[dict]:
    """Search facts via FactStore (Convex or local JSON)."""
    try:
        store = _get_fact_store(cfg)
        items = store.search(query, limit=10)
        
        results = []
        for item in items:
            results.append({
                "id": item.get("_id", ""),
                "text": item.get("fact", ""),
                "category": item.get("category", ""),
                "confidence": item.get("confidence", 0.8),
                "accessCount": item.get("accessCount", 0),
                "agent": item.get("agent", ""),
                "source": "convex",
                "filepath": f"agentMemory:{item.get('category', '')}",
                "score_raw": item.get("confidence", 0.8),
            })
        
        if debug:
            print(f"  Facts ({store.backend}): {len(results)} results", file=sys.stderr)
        return results
    except Exception as e:
        if debug:
            print(f"  Facts exception: {e}", file=sys.stderr)
        return []


# =====================================================================
# Source 2: Vector embeddings (nomic)
# =====================================================================
def search_embeddings(query: str, cfg: dict, limit: int = 15, debug: bool = False) -> list[dict]:
    """Search workspace using vector embeddings."""
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
            print(f"  Embed cache error: {e}", file=sys.stderr)
        return []
    
    chunks = cache.get("chunks", [])
    if not chunks:
        return []
    
    query_vec = embed([query], cfg, debug)
    if not query_vec or not query_vec[0]:
        return []
    
    qv = query_vec[0]
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
            "source": "embed",
            "score_raw": round(sim, 4),
            "semantic_sim": round(sim, 4),
        })
    
    if debug:
        top = results[0]["score_raw"] if results else 0
        print(f"  Embed: {len(results)} results (top: {top})", file=sys.stderr)
    return results


# =====================================================================
# Source 3: QMD (BM25)
# =====================================================================
def search_qmd(query: str, limit: int = 15, debug: bool = False) -> list[dict]:
    """Search via QMD CLI."""
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
                "source": "qmd",
                "score_raw": item.get("score", 0) / 100.0 if item.get("score", 0) > 1 else item.get("score", 0),
                "title": item.get("title", ""),
            })
        
        if debug:
            print(f"  QMD: {len(results)} results", file=sys.stderr)
        return results
    except Exception as e:
        if debug:
            print(f"  QMD exception: {e}", file=sys.stderr)
        return []


# =====================================================================
# Source 4: Knowledge Graph
# =====================================================================
def search_graph(query: str, cfg: dict, debug: bool = False) -> list[dict]:
    """Search knowledge graph for related files."""
    ws = cfg["paths"]["workspace"]
    graph_path = os.path.join(ws, cfg["paths"]["knowledgeGraph"])
    
    try:
        with open(graph_path) as f:
            graph = json.load(f)
    except Exception:
        if debug:
            print("  Graph: not found", file=sys.stderr)
        return []
    
    entities = graph.get("entities", {})
    query_lower = query.lower()
    query_words = set(query_lower.split())
    results = []
    
    # Support dict or list format
    if isinstance(entities, dict):
        items = list(entities.items())
    elif isinstance(entities, list):
        items = [(e.get("name", ""), e) for e in entities if isinstance(e, dict)]
    else:
        return []
    
    for name, data in items:
        name_l = name.lower()
        if name_l not in query_lower and query_lower not in name_l:
            # Check if any query word matches entity name
            if not any(w in name_l for w in query_words if len(w) > 2):
                continue
        
        # Get related files
        files = set()
        for f in data.get("mentions", []):
            files.add(f)
        for rel in data.get("relations", []):
            if isinstance(rel, dict):
                target = rel.get("target", "")
                if target:
                    files.add(target)
        
        # Score by relevance — filter out low-relevance files
        for f in files:
            f_lower = f.lower()
            score = sum(1 for w in query_words if w in f_lower) / max(len(query_words), 1)
            
            # Boost files likely relevant to query
            if "memory/" in f_lower or "bugs/" in f_lower:
                score += 0.3
            if name_l in f_lower:
                score += 0.2
            
            # Skip low-scoring graph results (etudes, exercices, etc. for a "bugs" query)
            if score < 0.15:
                continue
            
            results.append({
                "filepath": f,
                "line": 1,
                "text": f"[graph:{name}] {f}",
                "source": "graph",
                "score_raw": min(score, 1.0),
                "entity": name,
                "centrality": len(data.get("relations", [])),
            })
    
    # Cap graph results to avoid flooding merge
    results.sort(key=lambda r: -r["score_raw"])
    results = results[:20]
    
    if debug:
        print(f"  Graph: {len(results)} results", file=sys.stderr)
    return results


# =====================================================================
# Merge + Dedup
# =====================================================================
def merge_results(sources: list[list[dict]]) -> list[dict]:
    """Merge results from all sources, dedup by filepath."""
    seen = {}  # filepath → best result
    
    for source_results in sources:
        for r in source_results:
            key = r.get("filepath", "") + ":" + str(r.get("line", ""))
            
            if r.get("source") == "convex":
                # Convex results are unique by fact text
                key = "convex:" + r.get("text", "")[:80]
            
            if key not in seen:
                r["sources"] = [r.get("source", "?")]
                seen[key] = r
            else:
                # Merge: accumulate sources, keep best raw score
                existing = seen[key]
                existing["sources"].append(r.get("source", "?"))
                if r.get("score_raw", 0) > existing.get("score_raw", 0):
                    existing["score_raw"] = r["score_raw"]
                # Carry over specific fields
                if r.get("semantic_sim"):
                    existing["semantic_sim"] = r["semantic_sim"]
                if r.get("accessCount"):
                    existing["accessCount"] = r["accessCount"]
                if r.get("centrality"):
                    existing["centrality"] = r["centrality"]
    
    return list(seen.values())


# =====================================================================
# Multi-signal scoring
# =====================================================================
def extract_date_from_path(filepath: str) -> datetime | None:
    """Extract date from filepath."""
    m = re.search(r'(\d{4}-\d{2}-\d{2})', filepath)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    return None


def compute_recency(filepath: str, half_life_days: float = 14.0) -> float:
    """Compute recency score (0-1). Recent = higher."""
    # Protected categories don't decay
    for prefix in ["bugs/", "agents/", "infra/", "etudes/"]:
        if filepath.startswith(prefix):
            return 0.7  # Stable, no decay
    
    dt = extract_date_from_path(filepath)
    if dt is None:
        return 0.4  # Unknown date
    
    days_old = (datetime.now() - dt).days
    if days_old < 1:
        return 1.0
    return math.exp(-0.693 * days_old / half_life_days)


def score_result(r: dict, cfg: dict) -> float:
    """Compute composite score using 6 signals."""
    w = SCORE_WEIGHTS
    half_life = cfg["search"].get("decayHalfLifeDays", 14)
    
    # S1: Semantic similarity (from embed)
    semantic = r.get("semantic_sim", 0.0)
    
    # S2: BM25 score (from QMD)
    bm25 = r.get("score_raw", 0.0) if "qmd" in r.get("sources", []) else 0.0
    
    # S3: Recency
    recency = compute_recency(r.get("filepath", ""), half_life)
    
    # S4: Access frequency (from agentMemory)
    access = min(r.get("accessCount", 0) / 10.0, 1.0)  # Normalize: 10+ accesses = max
    
    # S5: Source trust
    best_trust = max(SOURCE_TRUST.get(s, 0.3) for s in r.get("sources", ["?"]))
    # Multi-source bonus: found by 2+ sources = more trustworthy
    if len(r.get("sources", [])) > 1:
        best_trust = min(best_trust + 0.15, 1.0)
    
    # S6: Graph centrality
    centrality = min(r.get("centrality", 0) / 15.0, 1.0)  # Normalize: 15+ relations = max
    
    composite = (
        w["semantic"] * semantic +
        w["bm25"] * bm25 +
        w["recency"] * recency +
        w["access"] * access +
        w["trust"] * best_trust +
        w["graph"] * centrality
    )
    
    return round(composite, 4)


def score_all(results: list[dict], cfg: dict) -> list[dict]:
    """Score and sort all results."""
    for r in results:
        r["composite_score"] = score_result(r, cfg)
    
    results.sort(key=lambda r: -r["composite_score"])
    return results


# =====================================================================
# LLM Reranker
# =====================================================================
def rerank(question: str, results: list[dict], cfg: dict, top: int = 8, debug: bool = False) -> list[dict]:
    """Use LLM to rerank top results by relevance to question."""
    if len(results) <= top:
        return results
    
    candidates = results[:top * 2]  # Take top 2x for reranking
    
    context = "\n".join([
        f"[{i}] ({r.get('source', '?')}) {r.get('filepath', '?')}: {r.get('text', '')[:200]}"
        for i, r in enumerate(candidates)
    ])
    
    prompt = f"""Question: {question}

Rank these search results by relevance to the question.
Return a JSON array of indices (0-based) in order of relevance, most relevant first.
Only include truly relevant results (skip irrelevant ones).

Results:
{context}

Respond with ONLY a JSON array of integers, e.g. [3, 0, 7, 1]"""
    
    ranking = call_llm_json(prompt, cfg, debug)
    
    if ranking and isinstance(ranking, list):
        reranked = []
        for idx in ranking:
            if isinstance(idx, int) and 0 <= idx < len(candidates):
                reranked.append(candidates[idx])
        if reranked:
            if debug:
                print(f"  Rerank: {len(candidates)} → {len(reranked)} results", file=sys.stderr)
            return reranked[:top]
    
    # Fallback: return top N by composite score
    return results[:top]


# =====================================================================
# Synthesis
# =====================================================================
def synthesize(question: str, results: list[dict], cfg: dict, debug: bool = False) -> dict:
    """Synthesize answer from top results."""
    if not results:
        return {"answer": "No results found.", "confidence": 0.0, "sources": []}
    
    context = "\n".join([
        f"[{r.get('filepath', '?')}] (score:{r.get('composite_score', 0):.2f}, via:{'+'.join(r.get('sources', []))}) {r.get('text', '')[:400]}"
        for r in results[:10]
    ])
    
    prompt = f"""Question: {question}

Context from multiple memory sources:
{context}

Answer the question based on the context. Be precise and cite sources.
If the context doesn't contain enough information, say so.

Respond in JSON:
{{"answer": "your answer", "confidence": 0.0-1.0, "sources": ["file1.md", "file2.md"]}}"""
    
    # Try JSON first
    result = call_llm_json(prompt, cfg, debug)
    if result and result.get("answer"):
        return result
    
    # Fallback: plain text synthesis (no JSON requirement)
    fallback_prompt = f"""Question: {question}

Memory context:
{context}

Answer the question based on the context. Be precise and cite source files.
Si le contexte ne contient pas assez d'info, dis-le."""
    
    text = call_llm(fallback_prompt, cfg, debug)
    if text:
        # Extract source files mentioned in text
        sources = re.findall(r'(?:memory/|agents/|bugs/|projects/|echanges/)[\w./-]+\.md', text)
        return {"answer": text[:2000], "confidence": 0.6, "sources": list(set(sources))[:5]}
    
    return {"answer": "Synthesis failed.", "confidence": 0.0, "sources": []}


# =====================================================================
# Main pipeline
# =====================================================================
def recall(question: str, cfg: dict | None = None, top: int = 8,
           do_rerank: bool = True, do_synthesize: bool = True,
           debug: bool = False) -> dict:
    """
    Unified recall pipeline.
    Fan-out → merge → score → rerank → synthesize.
    """
    t0 = time.time()
    if cfg is None:
        cfg = load_config(script="recall")
    
    # Phase 1: Fan-out (parallel)
    if debug:
        print("Phase 1: Fan-out...", file=sys.stderr)
    
    sources = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {
            pool.submit(search_convex, question, debug): "convex",
            pool.submit(search_embeddings, question, cfg, 15, debug): "embed",
            pool.submit(search_qmd, question, 15, debug): "qmd",
            pool.submit(search_graph, question, cfg, debug): "graph",
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                sources[name] = future.result()
            except Exception as e:
                if debug:
                    print(f"  {name} failed: {e}", file=sys.stderr)
                sources[name] = []
    
    fanout_time = time.time() - t0
    
    # Phase 2: Merge + dedup
    if debug:
        counts = {k: len(v) for k, v in sources.items()}
        print(f"\nPhase 2: Merge ({counts})...", file=sys.stderr)
    
    merged = merge_results(list(sources.values()))
    
    # Phase 3: Multi-signal scoring
    if debug:
        print(f"Phase 3: Scoring {len(merged)} results...", file=sys.stderr)
    
    scored = score_all(merged, cfg)
    
    # Phase 4: Rerank (optional)
    if do_rerank and len(scored) > top:
        if debug:
            print(f"Phase 4: Reranking top {top*2} → {top}...", file=sys.stderr)
        final = rerank(question, scored, cfg, top, debug)
    else:
        final = scored[:top]
    
    pipeline_time = time.time() - t0
    
    # Phase 5: Synthesize (optional)
    answer = None
    if do_synthesize:
        if debug:
            print(f"Phase 5: Synthesis from {len(final)} results...", file=sys.stderr)
        answer = synthesize(question, final, cfg, debug)
    
    total_time = time.time() - t0
    
    result = {
        "answer": answer.get("answer") if answer else None,
        "confidence": answer.get("confidence", 0) if answer else None,
        "results": final,
        "stats": {
            "total_results": len(merged),
            "per_source": {k: len(v) for k, v in sources.items()},
            "fanout_time": round(fanout_time, 2),
            "pipeline_time": round(pipeline_time, 2),
            "total_time": round(total_time, 2),
        },
        "sources_cited": answer.get("sources", []) if answer else [],
    }
    
    # Feedback: log query for later analysis
    _log_feedback(question, result, cfg)
    
    return result


def _log_feedback(question: str, result: dict, cfg: dict):
    """Log recall query + results for feedback analysis."""
    try:
        ws = cfg.get("paths", {}).get("workspace", ".")
        feedback_dir = os.path.join(ws, ".cache", "recall-feedback")
        os.makedirs(feedback_dir, exist_ok=True)
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "confidence": result.get("confidence", 0),
            "total_results": result.get("stats", {}).get("total_results", 0),
            "per_source": result.get("stats", {}).get("per_source", {}),
            "total_time": result.get("stats", {}).get("total_time", 0),
            "top_results": [
                {
                    "filepath": r.get("filepath", ""),
                    "score": round(r.get("composite_score", 0), 4),
                    "sources": r.get("sources", []),
                    "useful": None,  # To be filled by feedback
                }
                for r in result.get("results", [])[:8]
            ],
        }
        
        # Append to JSONL log
        log_path = os.path.join(feedback_dir, "queries.jsonl")
        with open(log_path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass  # Never break pipeline for feedback logging


def feedback_stats(cfg: dict) -> dict:
    """Analyze feedback logs: which sources perform best, avg confidence, etc."""
    ws = cfg.get("paths", {}).get("workspace", ".")
    log_path = os.path.join(ws, ".cache", "recall-feedback", "queries.jsonl")
    
    if not os.path.exists(log_path):
        return {"error": "No feedback data yet"}
    
    queries = []
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    queries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    
    if not queries:
        return {"error": "No valid feedback entries"}
    
    total = len(queries)
    avg_conf = sum(q.get("confidence", 0) for q in queries) / total
    avg_time = sum(q.get("total_time", 0) for q in queries) / total
    
    # Source contribution stats
    source_hits = {}
    source_top1 = {}
    for q in queries:
        for i, r in enumerate(q.get("top_results", [])):
            for src in r.get("sources", []):
                source_hits[src] = source_hits.get(src, 0) + 1
                if i == 0:
                    source_top1[src] = source_top1.get(src, 0) + 1
    
    # Useful/not useful (if feedback provided)
    useful_count = sum(1 for q in queries for r in q.get("top_results", []) if r.get("useful") is True)
    not_useful_count = sum(1 for q in queries for r in q.get("top_results", []) if r.get("useful") is False)
    
    return {
        "total_queries": total,
        "avg_confidence": round(avg_conf, 3),
        "avg_time_seconds": round(avg_time, 2),
        "source_appearances_in_top8": source_hits,
        "source_top1": source_top1,
        "feedback_provided": useful_count + not_useful_count,
        "useful": useful_count,
        "not_useful": not_useful_count,
    }


def main():
    parser = argparse.ArgumentParser(description="Unified memory recall pipeline")
    parser.add_argument("question", nargs="?", help="Question to recall")
    parser.add_argument("--top", type=int, default=8, help="Top results to keep")
    parser.add_argument("--rerank", action="store_true", default=True, help="LLM reranking (default: on)")
    parser.add_argument("--no-rerank", action="store_true", help="Skip LLM reranking")
    parser.add_argument("--no-llm", action="store_true", help="Scoring only, no synthesis/rerank")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--json", action="store_true", help="Output full JSON")
    parser.add_argument("--preset", help="Config preset (ollama, openai)")
    parser.add_argument("--stats", action="store_true", help="Show feedback statistics")
    args = parser.parse_args()
    
    if args.stats:
        cfg = load_config(preset=args.preset, script="recall")
        stats = feedback_stats(cfg)
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return
    
    if not args.question:
        parser.error("question is required (unless --stats)")
    
    cfg = load_config(preset=args.preset, script="recall")
    
    do_rerank = not args.no_rerank and not args.no_llm
    do_synth = not args.no_llm
    
    result = recall(args.question, cfg, top=args.top,
                    do_rerank=do_rerank, do_synthesize=do_synth, debug=args.debug)
    
    if args.json:
        # Clean up non-serializable fields
        for r in result.get("results", []):
            r.pop("embedding", None)
            r.pop("vector", None)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        # Human-readable output
        stats = result["stats"]
        src = stats["per_source"]
        print(f"📡 Sources: convex={src.get('convex',0)} embed={src.get('embed',0)} qmd={src.get('qmd',0)} graph={src.get('graph',0)} → {stats['total_results']} merged")
        print(f"⏱  {stats['total_time']:.1f}s (fanout: {stats['fanout_time']:.1f}s)")
        
        if result.get("answer"):
            conf = result.get("confidence", 0)
            icon = "✅" if conf >= 0.7 else "💡" if conf >= 0.4 else "⚠"
            print(f"\n{icon} {result['answer']}")
            print(f"\n📊 Confidence: {int(conf*100)}%")
            if result.get("sources_cited"):
                print(f"📎 Sources: {', '.join(result['sources_cited'][:5])}")
        
        if args.debug:
            print(f"\n--- Top {len(result['results'])} results ---")
            for i, r in enumerate(result["results"]):
                sources_str = "+".join(r.get("sources", []))
                print(f"  {i+1}. [{r.get('composite_score',0):.3f}] ({sources_str}) {r.get('filepath','?')}: {r.get('text','')[:100]}")


if __name__ == "__main__":
    main()
