#!/usr/bin/env python3
"""
gen_spirit.py — 生成卖家精灵插件字段 JS evaluate 代码

策略：一次性提取插件容器 raw text，返回后由 Python 正则解析子字段。
JS 端只做 DOM 定位 + innerText 提取，不做正则（减少 JS 复杂度和出错率）。

用法:
  python3 gen_spirit.py          # 输出 JS 代码字符串
"""

import sys
from selector_registry import FIELDS


SPIRIT_FIELDS = [k for k, v in FIELDS.items() if v["source"] == "seller_spirit"]


def generate_js() -> str:
    container_cfg = FIELDS["spirit_container"]
    raw_cfg = FIELDS["spirit_raw"]

    fb0 = raw_cfg['fallbacks'][0] if raw_cfg['fallbacks'] else ''
    fb1 = raw_cfg['fallbacks'][1] if len(raw_cfg['fallbacks']) > 1 else ''

    js = f"""  // 卖家精灵插件
  const spiritCont = document.querySelector("{container_cfg['primary']}")
    || document.querySelector("{fb0}")
    || document.querySelector("{fb1}");
  r["spirit_found"] = !!spiritCont;
  if (spiritCont) {{
    r["spirit_raw"] = spiritCont.innerText?.substring(0, 2000);
  }} else {{
    const anySpirit = document.querySelector('[id*="seller-sprite"]')
      || document.querySelector('[class*="seller-spirit"]')
      || document.querySelector('[class*="SellerSpirit"]');
    if (anySpirit) {{
      r["spirit_found"] = true;
      r["spirit_raw"] = anySpirit.innerText?.substring(0, 2000);
      r["spirit_selector_hit"] = anySpirit.id || anySpirit.className?.substring(0, 80);
    }} else {{
      r["spirit_raw"] = null;
    }}
  }}"""
    return js


if __name__ == "__main__":
    print(generate_js())
