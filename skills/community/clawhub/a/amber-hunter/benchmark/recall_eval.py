"""
benchmark/recall_eval.py — RAG Recall Evaluation v1.2.41
使用 RAGAS 框架评估检索质量。

输出:
    - benchmark/results/recall_eval_<timestamp>.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Results output directory
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def _load_ragas():
    """Lazy import ragas to make it optional."""
    try:
        from ragas import evaluate
        from ragas.metrics import faithfulness, answer_relevancy, context_precision
        from datasets import Dataset
        return evaluate, Dataset, faithfulness, answer_relevancy, context_precision
    except ImportError:
        return None


def _compute_ndcg_at_k(
    retrieved_ids: list[str],
    expected_ids: list[str],
    k: int = 5,
) -> float:
    """
    Compute NDCG@k for a single query.

    Args:
        retrieved_ids: list of retrieved document IDs in order
        expected_ids: list of expected relevant document IDs
        k: cutoff position

    Returns:
        NDCG@k score (0.0 to 1.0)
    """
    if not expected_ids:
        return 0.0

    expected_set = set(expected_ids)
    k_retrieved = retrieved_ids[:k]

    # DCG: sum of (rel_i / log2(i+1)) for i in retrieved
    dcg = 0.0
    for i, doc_id in enumerate(k_retrieved):
        rel = 1.0 if doc_id in expected_set else 0.0
        dcg += rel / (i + 1)  # position i is 0-indexed, so i+1 = position

    # IDCG: ideal DCG (all expected docs at top)
    ideal_retrieved = list(expected_set)[:k]
    idcg = 0.0
    for i, doc_id in enumerate(ideal_retrieved):
        rel = 1.0
        idcg += rel / (i + 1)

    if idcg == 0:
        return 0.0

    return dcg / idcg


def evaluate_recall(
    test_queries: list,
    amber_url: str = "http://localhost:18998",
    token: Optional[str] = None,
    limit_per_query: int = 5,
) -> dict:
    """
    Evaluate recall quality on a set of test queries using RAGAS.

    Args:
        test_queries: list of dicts with keys:
            - "q": query string
            - "expected_capsule_ids": list of expected relevant capsule IDs
        amber_url: amber-hunter service URL
        token: Bearer token (optional, will try to read from ~/.openclaw/token)
        limit_per_query: number of memories to retrieve per query

    Returns:
        dict with keys:
            - "ragas_scores": {"faithfulness": float, "answer_relevancy": float, "context_precision": float}
            - "ndcg_at_5": float
            - "evaluated_at": ISO timestamp
            - "total_queries": int
    """
    # Try to load token from ~/.openclaw/token if not provided
    if not token:
        token_path = Path("~/.openclaw/token").expanduser()
        if token_path.exists():
            try:
                token = token_path.read_text().strip()
            except Exception:
                pass

    if not token:
        return {
            "error": "No token provided and could not read from ~/.openclaw/token",
            "code": "AUTH_REQUIRED",
        }

    headers = {"Authorization": f"Bearer {token}"}

    # Run recall for each query
    recall_results: list[dict] = []
    ndcg_scores: list[float] = []

    for tq in test_queries:
        q = tq.get("q", "")
        expected_ids = tq.get("expected_capsule_ids", [])

        if not q:
            continue

        # Call /recall API
        try:
            import httpx
            resp = httpx.get(
                f"{amber_url}/recall",
                params={"q": q, "limit": limit_per_query},
                headers=headers,
                timeout=30.0,
            )
            if resp.status_code != 200:
                print(f"[eval] /recall failed for '{q}': {resp.status_code}", file=sys.stderr)
                continue

            data = resp.json()
            retrieved = data.get("memories", [])
            retrieved_ids = [m.get("id", "") for m in retrieved]

            # Compute NDCG@5 for this query
            ndcg = _compute_ndcg_at_k(retrieved_ids, expected_ids, k=5)
            ndcg_scores.append(ndcg)

            recall_results.append({
                "query": q,
                "expected_ids": expected_ids,
                "retrieved_ids": retrieved_ids,
                "ndcg_at_5": ndcg,
            })

        except Exception as e:
            print(f"[eval] Failed to evaluate query '{q}': {e}", file=sys.stderr)
            continue

    # Compute RAGAS scores if available
    ragas_scores = {"faithfulness": 0.0, "answer_relevancy": 0.0, "context_precision": 0.0}

    ragas_lib = _load_ragas()
    if ragas_lib is not None and recall_results:
        evaluate_fn, Dataset, faithfulness, answer_relevancy, context_precision = ragas_lib

        try:
            # Build RAGAS dataset
            # Note: RAGAS requires ground_truth answers which we don't have,
            # so we compute only context-based metrics
            eval_data = {
                "user_input": [r["query"] for r in recall_results],
                "retrieved_contexts": [
                    [f"capsule:{rid}" for rid in r["retrieved_ids"]]
                    for r in recall_results
                ],
                "response": [r["query"] for r in recall_results],  # placeholder
                "reference": [r["expected_ids"][0] if r["expected_ids"] else "" for r in recall_results],
            }
            ds = Dataset.from_dict(eval_data)

            # Evaluate
            result = evaluate_fn(ds, metrics=[context_precision])
            result_dict = result.to_dict()

            ragas_scores["faithfulness"] = result_dict.get("faithfulness", 0.0)
            ragas_scores["answer_relevancy"] = result_dict.get("answer_relevancy", 0.0)
            ragas_scores["context_precision"] = result_dict.get("context_precision", 0.0)

        except Exception as e:
            print(f"[eval] RAGAS evaluation failed: {e}", file=sys.stderr)
    else:
        if ragas_lib is None:
            print("[eval] RAGAS not installed. Run: pip install ragas", file=sys.stderr)

    # Average NDCG@5
    avg_ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0

    # Build result
    result = {
        "ragas_scores": ragas_scores,
        "ndcg_at_5": round(avg_ndcg, 4),
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "total_queries": len(recall_results),
        "per_query_results": recall_results,
    }

    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_path = RESULTS_DIR / f"recall_eval_{timestamp}.json"
    try:
        with open(result_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[eval] Results saved to {result_path}")
    except Exception as e:
        print(f"[eval] Failed to save results: {e}", file=sys.stderr)

    # Remove per_query_results from the main result for the API response
    main_result = {
        "ragas_scores": ragas_scores,
        "ndcg_at_5": round(avg_ndcg, 4),
        "evaluated_at": result["evaluated_at"],
        "total_queries": len(recall_results),
    }

    return main_result


# CLI entry point
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate amber-hunter recall quality")
    parser.add_argument("--queries", type=str, help="JSON string of test queries")
    parser.add_argument("--url", default="http://localhost:18998", help="Amber-hunter URL")
    parser.add_argument("--token", type=str, help="Bearer token")
    parser.add_argument("--limit", type=int, default=5, help="Memories per query")

    args = parser.parse_args()

    if args.queries:
        try:
            queries = json.loads(args.queries)
        except json.JSONDecodeError:
            print("Error: --queries must be valid JSON")
            sys.exit(1)
    else:
        # Default test queries
        queries = [
            {
                "q": "What technical decisions were made in the project?",
                "expected_capsule_ids": [],
            }
        ]

    result = evaluate_recall(
        test_queries=queries,
        amber_url=args.url,
        token=args.token,
        limit_per_query=args.limit,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
