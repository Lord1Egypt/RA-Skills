#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _as_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, str):
        return x
    try:
        return json.dumps(x, ensure_ascii=False)
    except Exception:
        return str(x)


def build_natural_language(resp: Dict[str, Any]) -> str:
    """
    将 /api/v1/review/flow/by-ocr 返回组装为自然语言摘要。
    返回通常包含：
    - results：数组（1 条或 2 条）
      - disease_code / review_type / scenario_code / scenario_id
      - flow_id / flow_name / flow_version
      - final_decision / reasoning
    """
    results = resp.get("results")
    if isinstance(results, list) and results:
        blocks: List[str] = []
        for r in results:
            if not isinstance(r, dict):
                continue
            disease_code = r.get("disease_code")
            review_type = r.get("review_type")
            scenario_code = r.get("scenario_code")
            scenario_id = r.get("scenario_id")
            flow_id = r.get("flow_id")
            flow_name = r.get("flow_name")
            flow_version = r.get("flow_version")
            final_decision = r.get("final_decision")
            reasoning = r.get("reasoning")

            lines: List[str] = []
            title = " / ".join([x for x in [_as_text(disease_code), _as_text(review_type)] if x])
            if title:
                lines.append(title)
            if final_decision is not None:
                lines.append(f"结论：{_as_text(final_decision)}")
            meta = []
            if scenario_code:
                meta.append(f"scenario_code={_as_text(scenario_code)}")
            if scenario_id is not None:
                meta.append(f"scenario_id={_as_text(scenario_id)}")
            if flow_id is not None:
                meta.append(f"flow_id={_as_text(flow_id)}")
            if flow_name:
                meta.append(f"flow_name={_as_text(flow_name)}")
            if flow_version:
                meta.append(f"flow_version={_as_text(flow_version)}")
            if meta:
                lines.append("元信息：" + "，".join(meta))
            if reasoning:
                lines.append("原因：" + _as_text(reasoning))
            blocks.append("\n".join(lines).strip())

        if blocks:
            return "\n\n---\n\n".join(blocks)

    if resp.get("success") is False:
        return "审核失败：" + _as_text(resp.get("error") or resp)

    return "已返回审核结果，但未找到 results 字段。原始返回请查看保存的 JSON。"


def main() -> int:
    parser = argparse.ArgumentParser(description="Format /review/flow response JSON to natural language.")
    parser.add_argument("--input", required=True, help="Path to response JSON.")
    parser.add_argument("--output", default="", help="Optional output text file path.")
    args = parser.parse_args()

    in_path = Path(args.input)
    resp = json.loads(in_path.read_text(encoding="utf-8"))
    text = build_natural_language(resp)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

