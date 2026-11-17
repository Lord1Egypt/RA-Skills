from __future__ import annotations

import json
import os
from pathlib import Path

from guard_core import check_security_v2, optimize_prompt_v1


FIXTURE_PATH = Path(__file__).resolve().parent.parent / "references" / "test_prompts.json"


def main() -> None:
    failures = []
    for line_number, case in enumerate(json.loads(FIXTURE_PATH.read_text(encoding="utf-8")), start=1):
        result = check_security_v2(case["message"], enable_semantic=False)
        if result["suggested_action"] != case["expected_action"]:
            failures.append((line_number, "suggested_action", case["expected_action"], result["suggested_action"]))
        if result["detector"] != case["expected_detector"]:
            failures.append((line_number, "detector", case["expected_detector"], result["detector"]))

    if failures:
        for line_number, field, expected, actual in failures:
            print(f"FAIL line {line_number}: {field} expected {expected!r}, got {actual!r}")
        raise SystemExit(1)

    optimization_result = optimize_prompt_v1("make a product launch video")
    if optimization_result["optimized"] or optimization_result["implemented"]:
        print("FAIL optimization stub: reserved module must not report implemented optimization.")
        raise SystemExit(1)

    malformed_result = check_security_v2({"message": "not a string"}, enable_semantic=False)
    if malformed_result["suggested_action"] != "BLOCK" or malformed_result["detector"] != "input_validation":
        print("FAIL malformed input: non-string input must be blocked by input_validation.")
        raise SystemExit(1)

    original_local_only = os.environ.get("GENAI_SECURITY_LOCAL_ONLY")
    original_model = os.environ.get("GENAI_SECURITY_MODEL")
    original_templates = os.environ.get("GENAI_SECURITY_TEMPLATES")
    os.environ["GENAI_SECURITY_LOCAL_ONLY"] = "1"
    os.environ["GENAI_SECURITY_MODEL"] = str(FIXTURE_PATH.parent / "missing_model")
    os.environ["GENAI_SECURITY_TEMPLATES"] = str(FIXTURE_PATH.parent / "missing_templates.json")
    semantic_failure = check_security_v2("Please summarize this ordinary paragraph.", enable_semantic=True)
    if semantic_failure["suggested_action"] != "BLOCK" or semantic_failure["detector"] not in {
        "semantic_error",
        "semantic_timeout",
    }:
        print("FAIL semantic failure: upstream failure must fail closed with BLOCK.")
        raise SystemExit(1)
    if original_local_only is None:
        os.environ.pop("GENAI_SECURITY_LOCAL_ONLY", None)
    else:
        os.environ["GENAI_SECURITY_LOCAL_ONLY"] = original_local_only
    if original_model is None:
        os.environ.pop("GENAI_SECURITY_MODEL", None)
    else:
        os.environ["GENAI_SECURITY_MODEL"] = original_model
    if original_templates is None:
        os.environ.pop("GENAI_SECURITY_TEMPLATES", None)
    else:
        os.environ["GENAI_SECURITY_TEMPLATES"] = original_templates

    print("Smoke tests passed.")


if __name__ == "__main__":
    main()
