#!/usr/bin/env python3
"""
gen_bsr.py — 生成 BSR/排名字段 JS evaluate 代码（body 片段，不含 IIFE）

从 selector_registry 读取选择器，避免硬编码。

用法:
  python3 gen_bsr.py          # 输出 JS body 片段
"""

import sys
from selector_registry import FIELDS


def _sel(field_id, key="primary"):
    cfg = FIELDS.get(field_id)
    if cfg:
        return cfg.get(key)
    return None


def _fallbacks(field_id):
    cfg = FIELDS.get(field_id)
    if cfg:
        return cfg.get("fallbacks", [])
    return []


def generate_js() -> str:
    db_primary = _sel("detail_bullets")
    db_fbs = _fallbacks("detail_bullets")

    db_fb0 = db_fbs[0] if len(db_fbs) > 0 else "null"
    db_fb1 = db_fbs[1] if len(db_fbs) > 1 else "null"
    db_fb2 = db_fbs[2] if len(db_fbs) > 2 else "null"

    spirit_primary = _sel("spirit_container", "primary")

    js = f"""  // BSR 排名
  const detail = document.querySelector("{db_primary}")
    || document.querySelector("{db_fb0}")
    || document.querySelector("{db_fb1}")
    || document.querySelector("{db_fb2}");
  if (detail) {{
    const text = detail.innerText;
    const bsrMatch = text.match(/Best Sellers Rank[:\\s]*([\\s\\S]*?)(?:\\n\\n|$)/);
    if (bsrMatch) {{
      r["bsr_raw"] = bsrMatch[1].trim().substring(0, 300);
    }}
  }}
  const spiritBsr = document.querySelector("{spirit_primary}");
  if (spiritBsr) {{
    const sText = spiritBsr.innerText;
    const rankMatches = sText.match(/#\\d+ in [^\\n]+/g);
    if (rankMatches) {{
      r["bsr_spirit"] = rankMatches;
    }}
  }}"""
    return js


if __name__ == "__main__":
    print(generate_js())