"""
真实聊天样例 -> 实际 skill 输出 的集成测试脚本。

不会 mock 搜索结果，会直接调用当前 skill 和后端接口。

运行：
  python test_chat_to_result.py
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from egatee_search_skill import EgateeSearchSkill, SearchConfig


def _build_cases() -> List[Dict[str, Any]]:
    """
    聊天记录样例（可按你们实际聊天结构继续补充）。
    """
    api_key = os.getenv("EGATEE_SEARCH_API_KEY", "").strip()
    common_meta: Dict[str, Any] = {"country": "UG", "top_k": 10}
    if api_key:
        common_meta["api_key"] = api_key

    return [
        {
            "name": "chat_text_simple",
            "payload": {
                "text": "找充电宝",
                "metadata": common_meta,
            },
        },
        {
            "name": "chat_text_query_field",
            "payload": {
                "query": "jersey white real madrid",
                "metadata": common_meta,
            },
        },
        {
            "name": "chat_image_attachment",
            "payload": {
                "text": "找同款",
                "attachments": [
                    {
                        "type": "image",
                        "url": "https://image.egatee.com/resources/2025/4/9/1744193139410.jpg_400x400.jpg",
                    }
                ],
                "metadata": common_meta,
            },
        },
        {
            "name": "chat_image_url_direct",
            "payload": {
                "mode": "image",
                "image_url": "https://image.egatee.com/resources/2025/4/9/1744193139410.jpg_400x400.jpg",
                "metadata": common_meta,
            },
        },
    ]


def _extract_brief(out: Dict[str, Any]) -> Dict[str, Any]:
    products = out.get("products", [])
    cards = out.get("cards", [])
    gt_cards = out.get("graphic_text_cards", [])
    top_titles = []
    for p in products[:3]:
        if isinstance(p, dict):
            top_titles.append(str(p.get("title", "")))
    return {
        "mode": out.get("mode"),
        "success": out.get("success"),
        "summary": out.get("summary"),
        "products_count": len(products) if isinstance(products, list) else None,
        "cards_count": len(cards) if isinstance(cards, list) else None,
        "graphic_text_cards_count": len(gt_cards) if isinstance(gt_cards, list) else None,
        "top_titles": top_titles,
    }


def main() -> int:
    base_url = os.getenv("EGATEE_SEARCH_BASE_URL", os.getenv("OPENCLAW_SEARCH_BASE_URL", "http://121.40.43.22:3004"))
    skill = EgateeSearchSkill(SearchConfig(base_url=base_url))
    cases = _build_cases()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = Path(__file__).resolve().parent / f"chat_result_samples_{ts}.json"
    all_results: List[Dict[str, Any]] = []

    print(f"Base URL: {base_url}")
    rem = skill.remaining_today()
    print(f"Remaining today: {'unlimited (verified api key)' if rem is None else rem}")
    print(f"Running cases: {len(cases)}")

    for idx, case in enumerate(cases, start=1):
        name = case["name"]
        payload = case["payload"]
        print(f"\n[{idx}/{len(cases)}] {name}")
        try:
            out = skill.run_from_chat(payload)
            brief = _extract_brief(out)
            print(json.dumps(brief, ensure_ascii=False, indent=2))
            all_results.append({"name": name, "ok": True, "payload": payload, "result": out, "brief": brief})
        except Exception as e:
            err = {"error": str(e)}
            print(json.dumps(err, ensure_ascii=False, indent=2))
            all_results.append({"name": name, "ok": False, "payload": payload, "error": str(e)})

    out_file.write_text(json.dumps({"generated_at": ts, "base_url": base_url, "cases": all_results}, ensure_ascii=False, indent=2), encoding="utf-8")
    ok_count = sum(1 for x in all_results if x.get("ok"))
    print(f"\nDone. success={ok_count}/{len(all_results)}")
    print(f"Output file: {out_file}")
    return 0 if ok_count == len(all_results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
