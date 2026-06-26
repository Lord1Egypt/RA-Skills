#!/usr/bin/env python3
"""
Recall Benchmark for Eidolon Search

Measures how well FTS5 retrieves relevant documents.
Recall@k = (relevant docs found in top k) / (total relevant docs)
"""

import sqlite3
import sys
import json
from pathlib import Path

BENCHMARK_QUERIES = [
    {
        "query": "Physical AI",
        "relevant_docs": [
            "memory/2026-03-01.md",
            "memory/physical-ai-roadmap.md"
        ]
    },
    {
        "query": "Triangle 완성",
        "relevant_docs": [
            "memory/projects-archive.md",
            "memory/2026-02-15.md"
        ]
    },
    {
        "query": "미라클 철학",
        "relevant_docs": [
            "MEMORY.md",
            "USER.md"
        ]
    },
    {
        "query": "Qdrant 설정",
        "relevant_docs": [
            "memory/eidolon-setup.md",
            "memory/2026-03-03.md"
        ]
    },
    {
        "query": "FTS5 최적화",
        "relevant_docs": [
            "memory/2026-03-03.md",
            "memory/search-performance.md"
        ]
    }
]

def search_fts(db_path: Path, query: str, limit: int = 10):
    """FTS5 검색"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT path, snippet(memory_fts, 1, '<b>', '</b>', '...', 32) as snippet, rank
        FROM memory_fts
        WHERE memory_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    results = cursor.fetchall()
    conn.close()
    
    return [{"path": r[0], "snippet": r[1], "rank": r[2]} for r in results]

def calculate_recall(found_paths: list, relevant_paths: list) -> float:
    """Recall 계산"""
    found_set = set(found_paths)
    relevant_set = set(relevant_paths)
    
    if len(relevant_set) == 0:
        return 0.0
    
    matches = found_set & relevant_set
    return len(matches) / len(relevant_set)

def run_benchmark(db_path: Path):
    """벤치마크 실행"""
    print("=" * 60)
    print("Recall Benchmark for Eidolon Search")
    print("=" * 60)
    print()
    
    results_summary = []
    
    for i, benchmark in enumerate(BENCHMARK_QUERIES, 1):
        query = benchmark["query"]
        relevant = benchmark["relevant_docs"]
        
        print(f"Query {i}: \"{query}\"")
        print(f"Relevant docs: {', '.join(relevant)}")
        
        # Search @5, @10
        for k in [5, 10]:
            results = search_fts(db_path, query, k)
            found_paths = [r["path"] for r in results]
            recall = calculate_recall(found_paths, relevant)
            
            print(f"  Recall@{k}: {recall:.2%} ({len([p for p in found_paths if p in relevant])}/{len(relevant)} found)")
            
            results_summary.append({
                "query": query,
                "k": k,
                "recall": recall,
                "found": len([p for p in found_paths if p in relevant]),
                "total_relevant": len(relevant)
            })
        
        print()
    
    # Overall stats
    recall_5 = [r["recall"] for r in results_summary if r["k"] == 5]
    recall_10 = [r["recall"] for r in results_summary if r["k"] == 10]
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Average Recall@5:  {sum(recall_5)/len(recall_5):.2%}")
    print(f"Average Recall@10: {sum(recall_10)/len(recall_10):.2%}")
    print()
    
    # Export JSON
    output = {
        "queries": BENCHMARK_QUERIES,
        "results": results_summary,
        "summary": {
            "avg_recall_5": sum(recall_5) / len(recall_5),
            "avg_recall_10": sum(recall_10) / len(recall_10)
        }
    }
    
    return output

if __name__ == "__main__":
    db_path = Path(__file__).parent.parent / "db" / "memory.db"
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        print("Run 'python scripts/build-index.py' first to create the index.")
        sys.exit(1)
    
    output = run_benchmark(db_path)
    
    # Save to file
    output_path = Path(__file__).parent.parent / "docs" / "benchmark-recall.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {output_path}")
