#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

import urllib.error
import urllib.parse
import urllib.request

from format_assessment_nl import build_natural_language


BASE_URL = "https://shangbao.yunzhisheng.cn/skills/critical-disease/api/v1/assessment/assess"

SUPPORTED_DISEASES = {
    "heart_valve_surgery",
    "aortic_surgery",
    "coronary_artery_bypass",
    "major_organ_transplant",
    "malignant_tumor",
    "severe_chronic_kidney_failure",
    "severe_chronic_liver_failure",
    "acute_severe_hepatitis",
    "severe_chronic_respiratory_failure",
    "severe_idiopathic_pulmonary_hypertension",
    "severe_brain_injury",
    "deep_coma",
    "severe_stroke_sequelae",
    "severe_alzheimers_disease",
    "severe_primary_parkinsons_disease",
    "severe_motor_neuron_disease",
    "severe_brain_encephalitis_sequelae",
    "severe_non_malignant_intracranial_tumor",
    "paralysis",
    "bilateral_deafness",
    "bilateral_blindness",
    "language_ability_loss",
    "severe_crohn_disease",
    "severe_ulcerative_colitis",
    "severe_aplastic_anemia",
    "moderate_acute_myocardial_infarction",
    "severe_third_degree_burn",
    "multiple_limb_loss",
}


def validate_payload(payload: Dict[str, Any]) -> None:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object")
    if "medicalRecord" not in payload or not isinstance(payload["medicalRecord"], dict):
        raise ValueError("Missing or invalid key: medicalRecord (object).")
    mr = payload["medicalRecord"]
    docs = mr.get("docs")
    if not isinstance(docs, list) or len(docs) == 0:
        raise ValueError("medicalRecord.docs must be a non-empty list.")
    has_doc_type = any(isinstance(d, dict) and d.get("docType") for d in docs)
    if not has_doc_type:
        raise ValueError("medicalRecord.docs must contain at least one item with docType.")


def call_major_disease_assess(
    disease: str,
    payload: Dict[str, Any],
    *,
    model_type: str = "qwq",
    timeout: int = 60,
) -> Dict[str, Any]:
    disease = (disease or "").strip()
    if not disease:
        raise ValueError("disease is required, e.g. aortic_surgery")
    if disease not in SUPPORTED_DISEASES:
        raise ValueError(f"Unsupported disease: {disease}. Supported: {sorted(SUPPORTED_DISEASES)}")

    validate_payload(payload)

    qs = urllib.parse.urlencode({"model_type": model_type})
    url = f"{BASE_URL}/{urllib.parse.quote(disease)}?{qs}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url=url, data=data, method="POST", headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def main() -> int:
    parser = argparse.ArgumentParser(description="Major disease (重大疾病) assessment via /assess/{disease}.")
    parser.add_argument("--disease", required=True, help="Disease type, e.g. aortic_surgery, heart_valve_surgery.")
    parser.add_argument("--input", required=True, help="Path to request JSON.")
    parser.add_argument(
        "--output-json",
        default="",
        help="Path to save raw response JSON (default: ../runs/med-major-disease-assess/{disease}_resp.json).",
    )
    parser.add_argument(
        "--output-text",
        default="",
        help="Path to save natural language summary (default: ../runs/med-major-disease-assess/{disease}_resp.txt).",
    )
    parser.add_argument("--model-type", default="qwq", help="Model type query param (default: qwq).")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds (default: 60).")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    payload = json.loads(in_path.read_text(encoding="utf-8"))

    try:
        # 先校验，后审核
        validate_payload(payload)
        resp = call_major_disease_assess(args.disease, payload, model_type=args.model_type, timeout=args.timeout)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    default_base = Path("../runs/med-major-disease-assess")
    out_json = Path(args.output_json) if args.output_json else (default_base / f"{args.disease}_resp.json")
    out_text = Path(args.output_text) if args.output_text else (default_base / f"{args.disease}_resp.txt")

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(resp, ensure_ascii=False, indent=2), encoding="utf-8")

    text = build_natural_language(resp)
    out_text.parent.mkdir(parents=True, exist_ok=True)
    out_text.write_text(text, encoding="utf-8")

    print(f"✓ Saved raw JSON to: {out_json}")
    print(f"✓ Saved natural language to: {out_text}")
    print("\n--- Natural language preview ---")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

