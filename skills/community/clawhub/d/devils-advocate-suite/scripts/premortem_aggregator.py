import json
import sys


def calculate_risk_score(likelihood, impact):
    """Score risks on a 1-25 matrix (1-5 each)."""
    return likelihood * impact


def categorize_risk(score):
    if score >= 20:
        return "CRITICAL"
    if score >= 12:
        return "HIGH"
    if score >= 6:
        return "MEDIUM"
    return "LOW"


def aggregate_failures(failure_list):
    """
    Input: List of dicts {"reason": str, "likelihood": 1-5, "impact": 1-5}
    Output: Aggregated report sorted by risk severity.
    """
    report = []
    for item in failure_list:
        score = calculate_risk_score(item["likelihood"], item["impact"])
        report.append(
            {
                "reason": item["reason"],
                "likelihood": item["likelihood"],
                "impact": item["impact"],
                "score": score,
                "category": categorize_risk(score),
            }
        )

    return sorted(report, key=lambda x: x["score"], reverse=True)


def print_risk_matrix(report):
    """Pretty-print the risk matrix to stdout."""
    print("\n=== RISK MATRIX ===\n")
    for item in report:
        bar = "█" * item["score"]
        print(f"[{item['category']:8}] Score {item['score']:2}/25 {bar}")
        print(f"           L={item['likelihood']} x I={item['impact']}: {item['reason']}\n")


if __name__ == "__main__":
    try:
        data = json.loads(sys.stdin.read())
        results = aggregate_failures(data)
        print_risk_matrix(results)
        print("\n--- JSON Output ---")
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error processing failure data: {e}")
        print("\nExpected input format (JSON array via stdin):")
        print('[{"reason": "...", "likelihood": 1-5, "impact": 1-5}, ...]')
