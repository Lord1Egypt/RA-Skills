#!/usr/bin/env python3
"""
healer.py — 选择器自愈：诊断断裂 + 生成修复方案

当 validate.py 报告 missing/suspicious 字段时：
1. 对缺失字段生成"诊断 JS"（搜索可能的新选择器）
2. 返回修复建议（新选择器 + 测试命令）

agent 执行流程:
  1. validate 报告 missing 字段 → 调 healer 生成诊断 JS
  2. agent 在浏览器执行诊断 JS → 得到候选选择器
  3. healer 根据候选结果生成修复建议
  4. agent 确认后更新 selectors.py

用法:
  python3 healer.py diagnose '<missing_fields_json>'      # 生成诊断 JS
  python3 healer.py propose '<diagnosis_result_json>'      # 根据诊断结果生成修复建议
  python3 healer.py apply '<field_id>' '<new_selector>'   # 更新 selectors.py
"""

import sys
import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SELECTORS_PATH = os.path.join(SCRIPT_DIR, "selector_registry.py")


def diagnose_missing(missing_fields: list) -> str:
    """为缺失字段生成诊断 JS：搜索页面中可能匹配的元素"""
    # 诊断策略：按字段语义搜索
    search_strategies = {
        "title": [
            'document.querySelectorAll("h1")',
            'document.querySelectorAll("[data-feature-name*=title]")',
        ],
        "price": [
            'document.querySelectorAll("[class*=price]")',
            'document.querySelectorAll("[id*=price]")',
        ],
        "rating": [
            'document.querySelectorAll("[class*=star], [class*=rating], [class*=acr]")',
            'document.querySelectorAll("[id*=acr]")',
        ],
        "review_count": [
            'document.querySelectorAll("[class*=review], [id*=review]")',
        ],
        "brand": [
            'document.querySelectorAll("[id*=brand], [class*=brand], [data-feature-name*=brand]")',
            'document.querySelectorAll("#bylineInfo, a[href*=brand]")',
        ],
        "seller": [
            'document.querySelectorAll("[id*=seller], [id*=soldBy], [class*=seller]")',
        ],
        "spirit_container": [
            'document.querySelectorAll("[id*=seller-sprite], [class*=seller-spirit], [class*=SellerSpirit]")',
        ],
        "sif_container": [
            'document.querySelectorAll("[data-sif], [class*=sif], [id*=sif]")',
        ],
        "deal_badge": [
            'document.querySelectorAll("[class*=deal], [class*=coupon], [id*=deal]")',
        ],
        "list_price": [
            'document.querySelectorAll("[class*=text-price], [class*=list-price], [aria-label*=List]")',
        ],
    }

    probes = []
    for field in missing_fields:
        strategies = search_strategies.get(field, [
            f'document.querySelectorAll("[id*=field], [class*=field]")',
        ])
        for selector in strategies:
            probes.append(f'probe("{field}", "{selector}")')

    js = f"""(() => {{
  const results = {{}};
  function probe(field, sel) {{
    try {{
      const els = document.querySelectorAll(sel);
      results[field + "|" + sel] = {{
        count: els.length,
        samples: Array.from(els).slice(0, 3).map(e => ({{
          tag: e.tagName,
          id: e.id?.substring(0, 60),
          cls: e.className?.substring(0, 80),
          text: e.innerText?.substring(0, 100),
          attrs: Object.keys(e.dataset || {{}}).join(",")
        }}))
      }};
    }} catch(e) {{
      results[field + "|" + sel] = {{error: e.message}};
    }}
  }}
  {"; ".join(probes)}
  return JSON.stringify(results, null, 1);
}})()"""
    return js


def propose_fixes(diagnosis_result: dict) -> list:
    """从诊断结果中提取修复建议"""
    proposals = []

    for key, info in diagnosis_result.items():
        if isinstance(info, dict) and info.get("error"):
            continue

        field_id, selector = key.split("|", 1)
        count = info.get("count", 0)
        samples = info.get("samples", [])

        if count == 0:
            continue

        # 唯一匹配（count=1）= 最佳候选
        for sample in samples:
            if sample.get("text") and len(sample["text"]) > 3:
                # 优先用 ID
                if sample.get("id"):
                    new_sel = f"#{sample['id']}"
                elif sample.get("cls"):
                    # 取第一个有效 class
                    first_cls = sample["cls"].split()[0]
                    new_sel = f".{first_cls}"
                else:
                    new_sel = f"{sample.get('tag', 'div')}[{selector.split('=')[1] if '=' in selector else ''}]"

                proposals.append({
                    "field": field_id,
                    "new_selector": new_sel,
                    "old_selector": selector,
                    "match_count": count,
                    "sample_text": sample["text"][:80],
                    "confidence": "high" if count == 1 else "medium",
                })

    return proposals


def apply_fix(field_id: str, new_selector: str) -> bool:
    """将修复的选择器写入 selectors.py"""
    with open(SELECTORS_PATH, "r") as f:
        content = f.read()

    # 找到对应字段的 primary 选择器行
    pattern = rf'("{field_id}":\s*\{{[^}}]*?"primary":\s*)"([^"]*)"'
    match = re.search(pattern, content)
    if not match:
        return False

    old_selector = match.group(2)
    # 把旧 primary 加到 fallbacks 首位，新选择器替换 primary
    new_content = content[:match.start()] + match.group(1) + f'"{new_selector}"' + content[match.end():]

    # 把旧 primary 加入 fallbacks（插入到第一个 fallback 之前）
    fallback_pattern = rf'("{field_id}":\s*\{{[^}}]*?"fallbacks":\s*\[)"([^"]*)"'
    fb_match = re.search(fallback_pattern, new_content)
    if fb_match and old_selector:
        insert_pos = fb_match.end(1)
        new_content = new_content[:insert_pos] + f'"{old_selector}", ' + new_content[insert_pos:]

    with open(SELECTORS_PATH, "w") as f:
        f.write(new_content)

    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法:")
        print("  python3 healer.py diagnose '<missing_fields_json>'")
        print("  python3 healer.py propose '<diagnosis_result_json>'")
        print("  python3 healer.py apply '<field_id>' '<new_selector>'")
        sys.exit(1)

    mode = sys.argv[1]
    input_data = sys.argv[2]

    if mode == "diagnose":
        missing = json.loads(input_data)
        js = diagnose_missing(missing)
        print(js)
    elif mode == "propose":
        diagnosis = json.loads(input_data)
        proposals = propose_fixes(diagnosis)
        print(json.dumps(proposals, ensure_ascii=False, indent=1))
    elif mode == "apply":
        field_id = input_data
        new_selector = sys.argv[3] if len(sys.argv) >= 4 else None
        if not new_selector:
            print("需要提供 new_selector 参数")
            sys.exit(1)
        success = apply_fix(field_id, new_selector)
        print(json.dumps({"success": success, "field": field_id, "new_primary": new_selector}))
    else:
        print(f"未知模式: {mode}")