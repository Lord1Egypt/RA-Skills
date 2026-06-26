#!/usr/bin/env python3
"""
gen_product.py — 生成 Amazon 产品基础字段 JS evaluate 代码

用法:
  python3 gen_product.py          # 输出 JS 代码字符串
  python3 gen_product.py --field  # 输出字段列表
"""

import sys
import json
import re
from selector_registry import FIELDS


AMAZON_FIELDS = [k for k, v in FIELDS.items() if v["source"] == "amazon_page"]


def _gen_try_block(field_id: str, cfg: dict) -> str:
    """为单个字段生成 try-catch + 主/备用选择器链"""
    extract = cfg["extract"]
    primary = cfg["primary"]
    fallbacks = cfg.get("fallbacks", [])

    # 特殊字段：从 URL 提取（无选择器）
    if primary is None and extract:
        return f'  r["{field_id}"] = {extract};'

    # 特殊字段：variant_names 使用 querySelectorAll
    if extract == "__QA__":
        lines = []
        lines.append(f'  try {{ r["{field_id}"] = (() => {{')
        lines.append(f'    const qa = document.querySelectorAll("{primary}");')
        lines.append(f'    if (qa.length) return Array.from(qa).map(e=>e.alt||e.title||e.getAttribute("aria-label")||"").filter(Boolean);')
        for i, fb_sel in enumerate(fallbacks):
            var = f"qa{i}"
            lines.append(f'    const {var} = document.querySelectorAll("{fb_sel}");')
            lines.append(f'    if ({var}.length) return Array.from({var}).map(e=>e.alt||e.title||e.getAttribute("aria-label")||"").filter(Boolean);')
        lines.append(f'    return null;')
        lines.append(f'  }})() }} catch(e) {{ r["{field_id}"] = null }}')
        return "\n".join(lines)

    lines = []
    lines.append(f'  try {{ r["{field_id}"] = (() => {{')
    lines.append(f'    const el = document.querySelector("{primary}");')
    lines.append(f'    if (el) return {extract.replace("el_selector", json.dumps(primary))};')
    # 备用选择器 - 每个用不同变量名
    for i, fb_sel in enumerate(fallbacks):
        var = f"fb{i}"
        lines.append(f'    const {var} = document.querySelector("{fb_sel}");')
        # 使用整词替换，避免把 querySelectorAll 等方法名中的 el 替换掉
        var_extract = re.sub(r'\bel\b', var, extract)
        var_extract = var_extract.replace("el_selector", json.dumps(fb_sel))
        lines.append(f'    if ({var}) return {var_extract};')
    lines.append(f'    return null;')
    lines.append(f'  }})() }} catch(e) {{ r["{field_id}"] = null }}')
    return "\n".join(lines)


def generate_js(field_ids=None) -> str:
    if field_ids is None:
        field_ids = AMAZON_FIELDS

    blocks = []
    for fid in field_ids:
        cfg = FIELDS.get(fid)
        if not cfg:
            continue
        blocks.append(_gen_try_block(fid, cfg))

    body = "\n".join(blocks)
    return body


if __name__ == "__main__":
    if "--field" in sys.argv:
        print(json.dumps(AMAZON_FIELDS))
    elif "--full" in sys.argv:
        body = generate_js()
        print(f"""(() => {{
  const r = {{}};
{body}
  return JSON.stringify(r, null, 1);
}})()""")
    else:
        print(generate_js())
