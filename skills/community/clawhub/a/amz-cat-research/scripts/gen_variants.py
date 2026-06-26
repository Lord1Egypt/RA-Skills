#!/usr/bin/env python3
"""
gen_variants.py — 生成变体字段 JS evaluate 代码（body 片段，不含 IIFE）

从 selector_registry 读取选择器，避免硬编码。

用法:
  python3 gen_variants.py          # 输出 JS body 片段
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
    var_primary = _sel("variant_container")
    var_fbs = _fallbacks("variant_container")
    fb0 = var_fbs[0] if len(var_fbs) > 0 else "null"
    fb1 = var_fbs[1] if len(var_fbs) > 1 else "null"

    name_primary = _sel("variant_names")
    name_fbs = _fallbacks("variant_names")

    lines = []
    lines.append("  // 变体信息")
    lines.append(f'  const twister = document.querySelector("{var_primary}")')
    lines.append(f'    || document.querySelector("{fb0}")')
    lines.append(f'    || document.querySelector("{fb1}");')
    lines.append('  r["has_variants"] = !!twister;')
    lines.append("  if (twister) {")
    all_variant_sel = ", ".join([name_primary] + name_fbs)
    lines.append(f'    const colorImgs = document.querySelectorAll("{all_variant_sel}");')
    lines.append('    if (colorImgs.length > 0) {')
    lines.append('      r["variant_names"] = Array.from(colorImgs).map(e => e.alt || e.title || e.getAttribute("aria-label") || "").filter(Boolean);')
    lines.append("    }")
    lines.append('    const sizeBtns = document.querySelectorAll("#variation_size_name button, [id*=\'size_name\'] button");')
    lines.append("    if (sizeBtns.length > 0) {")
    lines.append('      r["variant_sizes"] = Array.from(sizeBtns).map(e => e.innerText?.trim()).filter(Boolean);')
    lines.append("    }")
    lines.append('    const selectedSwatch = document.querySelector(".swatchElement.selected .a-button-text, [id*=\'variation\'] .selected");')
    lines.append("    if (selectedSwatch) {")
    lines.append('      r["variant_selected"] = selectedSwatch.innerText?.trim() || selectedSwatch.getAttribute("title") || "";')
    lines.append("    }")
    lines.append("  }")
    return "\n".join(lines)


if __name__ == "__main__":
    print(generate_js())