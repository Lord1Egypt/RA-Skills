#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

REPLACEMENTS = [
    ("[ノースフェイス]", "[노스페이스]"),
    ("[NIKE]", "[NIKE]"),
    ("[COYSEIO]", "[COYSEIO]"),
    ("[WOOALONG]", "[WOOALONG]"),

    ("ジャケット", "재킷"),
    ("バックパック", "백팩"),
    ("バッグ", "가방"),
    ("バケットバッグ", "버킷백"),
    ("ショルダー", "숄더"),
    ("トート", "토트"),
    ("クロスバッグ", "크로스백"),
    ("ジムサック", "짐색"),
    ("ベスト", "베스트"),
    ("フーディー", "후디"),
    ("ニット", "니트"),
    ("スウェットシャツ", "스웨트셔츠"),
    ("スウェット", "스웨트"),
    ("半袖 Tシャツ", "반소매 티셔츠"),
    ("半袖", "반소매"),
    ("Tシャツ", "티셔츠"),

    ("男女", "남녀"),
    ("女性", "여성"),
    ("レディース", "여성"),
    ("人気", "인기"),
    ("新作", "신작"),
    ("韓国", "한국"),
]

def translate_text(text: str) -> str:
    result = text
    for src, dst in REPLACEMENTS:
        result = result.replace(src, dst)
    return result

def main() -> None:
    parser = argparse.ArgumentParser(description="Build translated_names.json from raw_names.json")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    rows = json.loads(input_path.read_text(encoding="utf-8"))
    out = []

    for row in rows:
        order_no = str(row.get("order_no", "")).strip()
        product_name_ja = str(row.get("product_name_ja", "")).strip()
        if not order_no or not product_name_ja:
            continue
        out.append({
            "order_no": order_no,
            "product_name_ko": translate_text(product_name_ja)
        })

    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"count": len(out), "output": str(out_path)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
