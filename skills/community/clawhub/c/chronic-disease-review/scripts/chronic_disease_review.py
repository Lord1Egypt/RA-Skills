#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.error
import urllib.parse
import urllib.request

from format_review_nl import build_natural_language


DEFAULT_BASE = "https://shangbao.yunzhisheng.cn/skills/chronic-disease"

DISEASE_CODE_ALIASES: Dict[str, str] = {
    "diabetes": "糖尿病",
    "dm": "糖尿病",
    "糖尿病": "糖尿病",
    "hypertension": "高血压",
    "htn": "高血压",
    "高血压": "高血压",
}


def _http_json(method: str, url: str, *, payload: Optional[Dict[str, Any]] = None, timeout: int = 0) -> Any:
    data: Optional[bytes] = None
    headers: Dict[str, str] = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url=url, data=data, method=method, headers=headers)
    try:
        if timeout and timeout > 0:
            resp_ctx = urllib.request.urlopen(req, timeout=timeout)
        else:
            resp_ctx = urllib.request.urlopen(req)
        with resp_ctx as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body) if body.strip() else None
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def validate_ocr_data(ocr_data: Any) -> List[Dict[str, Any]]:
    if not isinstance(ocr_data, list) or len(ocr_data) == 0:
        raise ValueError("OCR input must be a non-empty JSON array (list).")
    out: List[Dict[str, Any]] = []
    for i, item in enumerate(ocr_data):
        if not isinstance(item, dict):
            raise ValueError(f"OCR item #{i} must be an object.")
        if not item.get("ocrText"):
            raise ValueError(f"OCR item #{i} missing required field: ocrText")
        if "page" in item and not isinstance(item["page"], int):
            raise ValueError(f"OCR item #{i} field page must be int when provided.")
        out.append(item)
    return out


def call_review_by_ocr(base: str, req_body: Dict[str, Any], *, timeout: int = 0) -> Dict[str, Any]:
    url = f"{base.rstrip('/')}/api/v1/review/flow/by-ocr"
    resp = _http_json("POST", url, payload=req_body, timeout=timeout)
    if not isinstance(resp, dict):
        raise RuntimeError(f"Invalid response from /review/flow/by-ocr: {resp}")
    return resp


def _resolve_disease_code(args_disease_code: str) -> Optional[str]:
    """
    disease_code 可选：
    - 传空：不填 disease_code（接口会两个都跑）
    - 传 diabetes/hypertension 等别名：映射到 中文 disease_code
    - 传中文糖尿病/高血压：原样
    """
    s = (args_disease_code or "").strip()
    if not s:
        return None
    if s in DISEASE_CODE_ALIASES:
        return DISEASE_CODE_ALIASES[s]
    return s


def _infer_label(disease_code: Optional[str]) -> str:
    if disease_code == "糖尿病":
        return "diabetes"
    if disease_code == "高血压":
        return "hypertension"
    return "by_ocr"


def _read_ocr_array(path: str) -> List[Dict[str, Any]]:
    """
    兼容两种用法：
    - 传现存路径
    - 只传文件名：若当前目录找不到，则尝试 skills/data/med-chronic-disease-review/<name>
    """
    p = Path(path)
    if not p.exists() and not p.is_absolute():
        fallback = Path(__file__).resolve().parents[2] / "data" / "med-chronic-disease-review" / p.name
        if fallback.exists():
            p = fallback
    raw = json.loads(p.read_text(encoding="utf-8"))
    return validate_ocr_data(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chronic disease review via POST /api/v1/review/flow/by-ocr.")
    parser.add_argument(
        "--disease-code",
        default="",
        help="Required disease_code: 糖尿病/高血压. Also supports aliases: diabetes/hypertension/dm/htn.",
    )
    parser.add_argument("--review-type", default="慢病审核", help="review_type (default: 慢病审核)")
    parser.add_argument("--input", required=True, help="Path to OCR array JSON (list).")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"Service base URL (default: {DEFAULT_BASE})")
    parser.add_argument("--llm-model", default="", help="Optional llm_model.")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP timeout seconds. 0 means wait forever (default: 0).")
    parser.add_argument("--output-json", default="", help="Path to save raw response JSON.")
    parser.add_argument("--output-text", default="", help="Path to save natural language summary.")
    args = parser.parse_args()

    try:
        disease_code = _resolve_disease_code(args.disease_code)
        if disease_code is None:
            raise ValueError("--disease-code is required (糖尿病/高血压 or diabetes/hypertension/dm/htn).")
        ocr_data = _read_ocr_array(args.input)
        req_body: Dict[str, Any] = {"review_type": (args.review_type or "慢病审核"), "ocr_data": ocr_data}
        req_body["disease_code"] = disease_code
        if args.llm_model:
            req_body["llm_model"] = args.llm_model

        resp = call_review_by_ocr(args.base, req_body, timeout=args.timeout)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    label = _infer_label(_resolve_disease_code(args.disease_code))
    default_base = Path("../runs/med-chronic-disease-review")
    out_json = Path(args.output_json) if args.output_json else (default_base / f"{label}_resp.json")
    out_text = Path(args.output_text) if args.output_text else (default_base / f"{label}_resp.txt")

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

