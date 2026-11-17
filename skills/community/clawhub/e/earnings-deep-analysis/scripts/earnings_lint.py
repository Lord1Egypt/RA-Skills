#!/usr/bin/env python3
"""财报深度解读报告硬闸脚本。

用法:
    python3 scripts/earnings_lint.py <报告HTML文件路径>

退出码:
    0 = 通过（无 FAIL，可有 WARN）
    1 = 有 WARN（建议项，可交付但需说明）
    2 = 有 FAIL（阻断项，禁止交付）
    3 = 用法错误（路径不存在等）

检查项:
    F01: 文件存在且可读
    F02: 文件是 HTML（含 <!DOCTYPE html> 或 <html）
    F03: 包含全部 13 个必需章节（h2 + id 匹配）
    F04: 每个章节有实质内容（非空、非纯占位符）
    F05: 无未替换的 {{...}} 占位符
    F06: 报告自包含（无外部 link/script src 引用）
    F07: 包含数据来源节且有至少1条来源
    W01: 核心结论条数 > 5（建议精简到3条以内）
    W02: 异常节未提及任何异常规则编号（A01-A15）
    W03: 投资含义节缺少"不构成投资建议"声明
"""

import re
import sys
import os

# 13 个必需章节
REQUIRED_SECTIONS = [
    ("core-conclusion", "核心结论"),
    ("overview", "业绩概览"),
    ("revenue", "收入分析"),
    ("gross-margin", "毛利率分析"),
    ("expenses", "费用分析"),
    ("profitability", "盈利能力"),
    ("cashflow", "现金流"),
    ("working-capital", "营运资本"),
    ("anomalies", "经营异常"),
    ("anomaly-causes", "异常原因"),
    ("risks", "风险"),
    ("investment-implications", "投资含义"),
    ("data-sources", "数据来源"),
]

# 占位符正则
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")

# 外部资源引用正则（link href 或 script src 指向 http）
EXTERNAL_REF_RE = re.compile(
    r'<(?:link[^>]+href|script[^>]+src)\s*=\s*["\']https?://', re.IGNORECASE
)


def lint(html_content: str):
    """返回 (fails, warns)，每个是 list[dict]。"""
    fails = []
    warns = []

    # F02: HTML 检测
    if "<!DOCTYPE html>" not in html_content and "<html" not in html_content.lower():
        fails.append({
            "code": "F02",
            "msg": "文件不是有效的 HTML（缺少 <!DOCTYPE html> 或 <html> 标签）",
            "fix": "确保报告以 <!DOCTYPE html> 开头并包含 <html> 根标签",
        })

    # F03: 必需章节检查
    found_sections = {}
    for sec_id, sec_name in REQUIRED_SECTIONS:
        # 检查 h2 标签中是否包含对应 id
        pattern = re.compile(
            r'<h2[^>]*\sid\s*=\s*["\']' + re.escape(sec_id) + r'["\']',
            re.IGNORECASE,
        )
        match = pattern.search(html_content)
        if not match:
            fails.append({
                "code": "F03",
                "msg": f"缺少必需章节：{sec_name}（id=\"{sec_id}\"）",
                "fix": f"在报告中添加 <h2 id=\"{sec_id}\">{sec_name}</h2> 章节",
            })
        else:
            found_sections[sec_id] = True

    # F04: 章节实质内容检查
    for sec_id, sec_name in REQUIRED_SECTIONS:
        if sec_id not in found_sections:
            continue  # F03 已报错，不重复
        # 用字符串查找法提取 h2 到下一个边界之间的内容
        h2_tag = re.compile(
            r'<h2[^>]*\sid\s*=\s*["\']' + re.escape(sec_id) + r'["\'][^>]*>',
            re.IGNORECASE,
        )
        m = h2_tag.search(html_content)
        if not m:
            continue  # F03 已报
        start = m.end()
        # 找到下一个边界：</section> 或 <h2 或 <div class="footer 或 </body
        boundaries = []
        for pat in [r'</section>', r'<h2', r'<div\s+class="footer"', r'</body>']:
            bm = re.compile(pat, re.IGNORECASE).search(html_content, start)
            if bm:
                boundaries.append(bm.start())
        end = min(boundaries) if boundaries else len(html_content)
        content = html_content[start:end]
        text = re.sub(r"<[^>]+>", "", content).strip()
        if len(text) < 10:
            fails.append({
                "code": "F04",
                "msg": f"章节「{sec_name}」内容过短（纯文本 < 10 字符），可能只有标题无实质内容",
                "fix": f"在「{sec_name}」章节中填入实质分析内容",
            })

    # F05: 未替换的占位符
    placeholders = PLACEHOLDER_RE.findall(html_content)
    if placeholders:
        fails.append({
            "code": "F05",
            "msg": f"发现 {len(placeholders)} 处未替换的占位符：{placeholders[:5]}",
            "fix": "将所有 {{...}} 占位符替换为实际内容",
        })

    # F06: 外部资源引用
    external_refs = EXTERNAL_REF_RE.findall(html_content)
    if external_refs:
        fails.append({
            "code": "F06",
            "msg": f"发现 {len(external_refs)} 处外部资源引用（link/script 指向 http），报告不自包含",
            "fix": "移除所有外部 link/script 引用，CSS 和 JS 全部内联",
        })

    # F07: 数据来源节检查
    ds_pattern = re.compile(
        r'<h2[^>]*\sid\s*=\s*["\']data-sources["\'][^>]*>.*?</h2>(.*?)(?=<h2|</section>)',
        re.DOTALL | re.IGNORECASE,
    )
    ds_match = ds_pattern.search(html_content)
    if ds_match:
        ds_content = ds_match.group(1)
        ds_text = re.sub(r"<[^>]+>", "", ds_content).strip()
        if len(ds_text) < 5:
            fails.append({
                "code": "F07",
                "msg": "数据来源节内容为空或过短",
                "fix": "在数据来源节列出至少 1 条数据来源",
            })
    # 如果 F03 已报 data-sources 缺失，不重复报 F07

    # W01: 核心结论条数
    cc_pattern = re.compile(
        r'<h2[^>]*\sid\s*=\s*["\']core-conclusion["\'][^>]*>.*?</h2>(.*?)(?=<h2|</section>)',
        re.DOTALL | re.IGNORECASE,
    )
    cc_match = cc_pattern.search(html_content)
    if cc_match:
        cc_content = cc_match.group(1)
        li_count = len(re.findall(r"<li", cc_content, re.IGNORECASE))
        if li_count > 5:
            warns.append({
                "code": "W01",
                "msg": f"核心结论有 {li_count} 条，建议精简到 3 条以内",
                "fix": "将核心结论精简到 3 条以内，按重要性排序",
            })

    # W02: 异常节是否提及规则编号
    anom_pattern = re.compile(
        r'<h2[^>]*\sid\s*=\s*["\']anomalies["\'][^>]*>.*?</h2>(.*?)(?=<h2|</section>)',
        re.DOTALL | re.IGNORECASE,
    )
    anom_match = anom_pattern.search(html_content)
    if anom_match:
        anom_content = anom_match.group(1)
        anom_text = re.sub(r"<[^>]+>", "", anom_content)
        rule_refs = re.findall(r"A\d{2}", anom_text)
        if not rule_refs and len(anom_text) > 20:
            warns.append({
                "code": "W02",
                "msg": "经营异常节未提及任何异常规则编号（A01-A15）",
                "fix": "在异常节中标注触发的规则编号（如 A01、A03 等）",
            })

    # W03: 投资含义节声明
    ii_pattern = re.compile(
        r'<h2[^>]*\sid\s*=\s*["\']investment-implications["\'][^>]*>.*?</h2>(.*?)(?=<h2|</section>)',
        re.DOTALL | re.IGNORECASE,
    )
    ii_match = ii_pattern.search(html_content)
    if ii_match:
        ii_content = ii_match.group(1)
        ii_text = re.sub(r"<[^>]+>", "", ii_content)
        if "不构成" not in ii_text and "投资建议" not in ii_text:
            warns.append({
                "code": "W03",
                "msg": "投资含义节缺少「不构成投资建议」声明",
                "fix": "在投资含义节末尾添加「本节不构成买入/卖出建议」声明",
            })

    return fails, warns


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/earnings_lint.py <报告HTML文件路径>")
        sys.exit(3)

    file_path = sys.argv[1]

    # F01: 文件存在
    if not os.path.isfile(file_path):
        print(f"FAIL F01: 文件不存在: {file_path}")
        sys.exit(3)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        print(f"FAIL F01: 无法读取文件: {e}")
        sys.exit(3)

    fails, warns = lint(html_content)

    # 输出结果
    if fails:
        print(f"=== {len(fails)} 个 FAIL（阻断项）===")
        for item in fails:
            print(f"  [{item['code']}] {item['msg']}")
            print(f"    修复: {item['fix']}")
        print()

    if warns:
        print(f"=== {len(warns)} 个 WARN（建议项）===")
        for item in warns:
            print(f"  [{item['code']}] {item['msg']}")
            print(f"    建议: {item['fix']}")
        print()

    if fails:
        print("结论: FAIL — 禁止交付，请修复后重跑。")
        sys.exit(2)
    elif warns:
        print("结论: PASS with WARN — 可交付，但建议处理上述 WARN。")
        sys.exit(1)
    else:
        print("结论: PASS — 全部检查通过，可交付。")
        sys.exit(0)


if __name__ == "__main__":
    main()
