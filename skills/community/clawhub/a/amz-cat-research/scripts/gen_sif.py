#!/usr/bin/env python3
"""
gen_sif.py — 生成 SIF 插件字段 JS evaluate 代码

策略：同卖家精灵，JS 只做 DOM 定位 + raw text，Python 端正则解析。

用法:
  python3 gen_sif.py          # 输出 JS 代码字符串
"""

import sys
from selector_registry import FIELDS


SIF_FIELDS = [k for k, v in FIELDS.items() if v["source"] == "sif"]


def generate_js() -> str:
    container_cfg = FIELDS["sif_container"]
    raw_cfg = FIELDS["sif_raw"]

    fb0 = raw_cfg['fallbacks'][0] if raw_cfg['fallbacks'] else ''
    fb1 = raw_cfg['fallbacks'][1] if len(raw_cfg['fallbacks']) > 1 else ''

    js = f"""  // SIF 插件
  const sifCont = document.querySelector("{container_cfg['primary']}")
    || document.querySelector("{fb0}")
    || document.querySelector("{fb1}");
  r["sif_found"] = !!sifCont;
  if (sifCont) {{
    r["sif_raw"] = sifCont.innerText?.substring(0, 1500);
  }} else {{
    const anySif = document.querySelector('[class*="sif-"]')
      || document.querySelector('[class*="SIF"]')
      || document.querySelector('[id*="sif"]');
    if (anySif) {{
      r["sif_found"] = true;
      r["sif_raw"] = anySif.innerText?.substring(0, 1500);
      r["sif_selector_hit"] = anySif.id || anySif.className?.substring(0, 80);
    }} else {{
      r["sif_raw"] = null;
    }}
  }}"""
    return js


if __name__ == "__main__":
    print(generate_js())
