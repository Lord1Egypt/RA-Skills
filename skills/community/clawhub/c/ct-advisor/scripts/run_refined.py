#!/usr/bin/env python3
"""ct-advisor answer refiner entry (in-process call + base64 CLI dual mode).

=== Preferred: in-process call (agent imports in a Python context, no encoding issues) ===
    import sys
    sys.path.insert(0, skill_dir)
    from scripts.run_refined import refine_direct

    answer = refine_direct(
        query_meta={"category": "design", "difficulty": "middle", "accuracy": "good"},
        original_question="设计一个III期双盲RCT评估新抗肿瘤药物的PFS终点",
        draft_answer="草稿...",
    )
    print(answer)

=== Alternative: base64 CLI (avoids Chinese-JSON encoding issues) ===
    PowerShell:
        $payload = @{query_meta='{...}'; original_question='...'} | ConvertTo-Json -Compress
        $b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($payload))
        python scripts/run_refined.py --payload-b64 $b64

query_meta is a JSON string or dict with three fields:
  - difficulty: simple | middle | complex | vague
  - category:   question category
  - accuracy:   self-rated accuracy good | normal
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.i18n import t  # noqa: E402  (user-facing prompts EN/ZH, locale-resolved)
from adapters import build_refiner, RefineRequest


def refine_direct(
    query_meta: dict | str,
    original_question: str,
    draft_answer: str,
    config_path: str = "config.json",
) -> str:
    """Call the refiner directly (no JSON encoding / command-line arg passing, fully avoids Chinese mojibake).

    Args:
        query_meta: dict or JSON string, containing category/difficulty/accuracy
        original_question: the user's raw question
        draft_answer: local draft
        config_path: path to config.json

    Returns:
        final answer string (Coze refined result or fallback draft)
    """
    req = RefineRequest(
        query_meta=query_meta,
        original_question=original_question,
        draft_answer=draft_answer,
    )
    # query_origin is auto-stamped into query_meta by normalize(); no top-level field.

    heal_notes = req.normalize()
    if heal_notes:
        sys.stderr.write(
            t("error.payload_healed", notes="; ".join(heal_notes)) + "\n"
        )

    try:
        req.validate()
    except ValueError as e:
        sys.stderr.write(
            t("error.payload_invalid", error=f"contract validation failed: {e}") + "\n"
        )
        if not draft_answer or not draft_answer.strip():
            return t("error.empty_question")
        return draft_answer

    try:
        refiner = build_refiner(config_path=config_path)
        return refiner.refine(req)
    except Exception as e:
        sys.stderr.write(
            t("error.refine_fallback", error=f"{type(e).__name__}: {e}") + "\n"
        )
        return draft_answer


def main() -> None:
    """CLI entry point (base64 payload mode, alternative)."""
    ap = argparse.ArgumentParser(description="ct-advisor answer refiner (base64 payload)")
    ap.add_argument("--payload-b64", required=True, help="Base64-encoded UTF-8 JSON payload")
    ap.add_argument("--config", default="config.json", help="path to config.json")
    ap.add_argument("--payload-b64", required=True, help="Base64-encoded UTF-8 JSON payload")
    args = ap.parse_args()

    # 1) Base64 decode → JSON string
    try:
        raw = base64.b64decode(args.payload_b64).decode("utf-8")
    except Exception as e:
        sys.stderr.write(
            t("error.base64_decode", error=f"{type(e).__name__}: {e}") + "\n"
        )
        sys.exit(1)

    # 2) Parse JSON
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        sys.stderr.write(
            t("error.payload_invalid", error=f"JSON parse failed: {type(e).__name__}: {e}") + "\n"
        )
        sys.exit(1)

    # 3) Call refine_direct
    answer = refine_direct(
        query_meta=obj.get("query_meta", ""),
        original_question=str(obj.get("original_question", "")),
        draft_answer=str(obj.get("draft_answer", "")),
        config_path=args.config,
    )
    sys.stdout.write(answer)


if __name__ == "__main__":
    main()
