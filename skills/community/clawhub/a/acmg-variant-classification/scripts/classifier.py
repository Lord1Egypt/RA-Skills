import json
import sys
from pathlib import Path


def classify(pathogenic: dict, benign: dict, conflict: bool = False) -> str:
    pv = pathogenic.get("very_strong", 0)
    ps = pathogenic.get("strong", 0)
    pm = pathogenic.get("moderate", 0)
    pp = pathogenic.get("supporting", 0)

    ba = benign.get("standalone", 0)
    bs = benign.get("strong", 0)
    bp = benign.get("supporting", 0)

    if conflict and (pv or ps or pm or pp) and (ba or bs or bp):
        return "VUS"

    if ba >= 1:
        return "Benign"
    if bs >= 2:
        return "Benign"

    if (
        (pv >= 1 and ps >= 1)
        or (pv >= 1 and pm >= 2)
        or (pv >= 1 and pm >= 1 and pp >= 1)
        or (pv >= 1 and pp >= 2)
        or (ps >= 2)
        or (ps >= 1 and pm >= 3)
        or (ps >= 1 and pm >= 2 and pp >= 2)
        or (ps >= 1 and pm >= 1 and pp >= 4)
        or (pm >= 3 and pp >= 3)
    ):
        return "Pathogenic"

    if (
        (pv >= 1 and pm >= 1)
        or (ps >= 1 and pm in (1, 2))
        or (ps >= 1 and pp >= 2)
        or (pm >= 3)
        or (pm >= 2 and pp >= 2)
        or (pm >= 1 and pp >= 4)
    ):
        return "Likely Pathogenic"

    if (bs >= 1 and bp >= 1) or (bp >= 2):
        return "Likely Benign"

    return "VUS"


def run_tests(cases: list[dict]) -> list[dict]:
    results = []
    for case in cases:
        got = classify(case["pathogenic"], case["benign"], case.get("conflict", False))
        results.append({
            "id": case["id"],
            "expected": case["expected"],
            "got": got,
            "pass": got == case["expected"],
        })
    return results


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "references" / "test_cases.json"
    cases = json.loads(path.read_text())
    results = run_tests(cases)
    passed = sum(r["pass"] for r in results)
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, ensure_ascii=False, indent=2))
    sys.exit(0 if passed == len(results) else 1)
