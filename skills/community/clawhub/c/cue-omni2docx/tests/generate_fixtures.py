#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_fixtures.py — 生成 omni2docx 回归套件的合成 fixture。

全部为虚构占位语料（与任何真实机构/个人无关），结构等价于真实语料，
保留断言锚点：引用块（楷体）、嵌套行内（code/链接/斜体）、emoji（剥离/保留）、
表格、脚注、截断、大文档、OCR 拆字。便于公开仓库可复现、无版权/隐私风险。

用法：python3 tests/generate_fixtures.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"

DISCLAIMER = "（本文件为回归测试合成语料，与任何真实机构、个人及数据无关）\n"

# ---------- 基础合成文档 ----------

D1_ETF = f"""# 示例交易型开放式指数基金（ETF）季度报告（合成语料）
{DISCLAIMER}
## 一、基金概况
示例 ETF 跟踪示例宽基指数，本报告期规模约为示例数值，跟踪误差在示例区间内。

## 二、主要持仓
| 证券名称 | 占净值比 | 所属行业 |
| --- | --- | --- |
| 示例银行 | 12.3% | 金融 |
| 示例能源 | 9.8% | 能源 |
| 示例科技 | 15.2% | 信息技术 |
| 示例医药 | 8.7% | 医药健康 |

## 三、风险提示
市场有风险，投资需谨慎。本示例文件仅供测试使用，不构成任何投资建议。
"""

D2_BOND = f"""# 示例公司债券募集说明书（摘要，合成语料）
{DISCLAIMER}
## 1. 发行要素
本期示例债券发行规模为示例金额，期限为示例年限，票面利率为示例水平。

## 2. 财务数据
| 年度 | 营业收入 | 净利润 |
| --- | --- | --- |
| 示例第一年 | 示例数值 | 示例数值 |
| 示例第二年 | 示例数值 | 示例数值 |
| 示例第三年 | 示例数值 | 示例数值 |

## 3. 偿债能力分析
示例分析内容，用于说明发行人偿债能力稳健，偿债保障措施充分。
"""

D3_LEGAL = f"""# 示例法律观察（合成语料）
{DISCLAIMER}
## 1. 行内嵌套
**加粗中包含 `code 片段` 与 [链接](https://example.com) 以及 *斜体*** 的混合行。

普通文本 `inline_code` 与 **bold** 与 *italic*，以及又一个 [示例链接](https://example.com/doc)。

## 2. 表情与装饰符 ✅ ❌ ★ ☆
示例内容含装饰符，用于测试装饰符剥离与保留两种路径。

## 3. 引用块
> 这是一段引用：正式文书要求楷体，且不应出现 emoji 😀。

## 4. 脚注
正文带脚注标记[^1]，以及第二个脚注[^note]。

[^1]: 第一个脚注的内容，含中文与 emoji 📌。
[^note]: 命名脚注内容，用于测试脚注渲染。

## 5. 表格
| 指标 | 数值 | 备注 |
| --- | --- | --- |
| 示例指标 ✅ | 12.3% | 含**加粗**单元格 |
| 示例波动率 | 8.1% | `code` 单元格 |
"""

D4_HTML = f"""# 示例学术综述（合成语料）
{DISCLAIMER}
## 摘要
本文示例性地讨论示例主题，不含任何真实研究结论，仅用于回归测试。

## 1. 背景
示例背景段落，说明研究动机与问题界定。

## 2. 方法
示例方法描述，包括数据来源与处理流程。

## 3. 结果与讨论
示例结果讨论，说明发现的示例性意义。

## 4. 结论
示例结论，指出后续示例方向。
"""

D4Q_HTML = D4_HTML + """
## 5. 引述与注释
> 这是一段示例引用，用于测试引用块在展示与汇报两种制式下的渲染。

正文带脚注标记[^1]，说明引用来源。

[^1]: 示例脚注内容，用于测试脚注渲染路径。
"""

D5_AUDIO = f"""# 示例音频转写稿（合成语料）
{DISCLAIMER}
## 说话人甲 00:00-00:30
示例发言内容：今天我们讨论示例话题，先介绍背景。

## 说话人乙 00:30-01:00
示例回应内容：同意上述观点，并补充示例论据。

## 说话人甲 01:00-01:30
示例追问内容：那么示例影响如何度量？

## 小结
示例小结，归纳讨论要点。
"""

D6_DOCX = f"""# 示例文档（自定义样式，合成语料）
{DISCLAIMER}
## 第一节
示例正文内容，用于测试自定义字体、字号与行距配置是否生效。

## 第二节
| 项目 | 数值 |
| --- | --- |
| 示例项甲 | 示例值一 |
| 示例项乙 | 示例值二 |

## 第三节
示例结尾段落，确认自定义样式下排版正常。
"""

D7_PPTX = f"""# 示例汇报材料（合成语料）
{DISCLAIMER}
## 要点一
- 示例子要点 A
- 示例子要点 B
- 示例子要点 C

## 要点二
- 示例子要点 D
- 示例子要点 E

## 要点三
示例说明：汇报版式将要点上页、正文进演讲者备注。
"""

D8_OCR = f"""# 示例 OCR 识别稿（合成语料）
{DISCLAIMER}
T h e y s h o w e d u s a n e x a m p l e o f t h e s y s t e m .

示例正常段落，含 emoji 📊 用于测试装饰符剥离路径。

## 说明
上述英文为示例 OCR 拆字，验证渲染不崩溃；中文正文保持正常覆盖。
"""

# D11：OCR 间距专项——CJK 逐字空格应被清理，拉丁逐字母空格属已知限制应保留
D11_OCR_SPACING = f"""# 示例 OCR 间距稿（合成语料）
{DISCLAIMER}
他 们 讨 论 了 方 案 的 细 节 ， 并 形 成 了 书 面 记 录 。

W e d i s c u s s e d t h e p l a n a n d r e c o r d e d i t .

示例正常段落：引擎应清理紧贴 CJK 字符的空格，但保留拉丁 OCR 拆字（已知限制，不在本引擎修复范围）。

## 对照说明
第一段为 CJK 逐字空格（应被 clean_cjk_spaces 去除）；第二段为拉丁逐字母空格（已知限制，应原样保留）。
"""

D10_TRUNC = f"""# 示例截断文档（合成语料）
{DISCLAIMER}
## 第一节
示例内容正常，段落完整。

## 第二节
本段故意截断，用于测试容错：后续分析应当包括市场结构、流动性与
"""

# D9 大文档：程序化生成多节，模拟规模而不含真实内容
def build_huge():
    parts = ["# 示例大规模文档（合成语料）", DISCLAIMER,
             "## 总述", "示例总述段落，说明本示例文档用于测试大规模输入的渲染与性能。"]
    for i in range(1, 41):
        parts.append(f"## 第 {i} 章 示例章节")
        parts.append(f"示例第 {i} 章正文，描述示例内容，用于扩充文档规模以验证分页与性能。")
        parts.append(f"| 维度 | 第{i}章值 |")
        parts.append("| --- | --- |")
        parts.append(f"| 示例维度甲 | 示例值{i} |")
        parts.append(f"| 示例维度乙 | 示例值{i} |")
    parts.append("## 末章 示例结论")
    parts.append("示例结论段落，结束本大规模合成文档。")
    return "\n".join(parts) + "\n"

DOCS = {
    "m01_etf_xlsx": D1_ETF,
    "m02_bond_pdf": D2_BOND,
    "m03_report_pdf": D3_LEGAL,
    "m04_html": D4_HTML,
    "m05_audio": D5_AUDIO,
    "m06_docx": D6_DOCX,
    "m07_pptx": D7_PPTX,
    "m08_jpg_ocr": D8_OCR,
    "m09_huge1000p": build_huge(),
    "m10_truncated": D10_TRUNC,
    "m11_ocr_spacing": D11_OCR_SPACING,
}

# docx 矩阵用的 .omni.md 文件名（中性名，去本机路径）
DOCX_NAMES = {
    "m01_etf_xlsx": "m01_etf_xlsx.omni.md",
    "m02_bond_pdf": "m02_bond_pdf.omni.md",
    "m03_report_pdf": "m03_report_pdf.omni.md",
    "m04_html": "m04_html.omni.md",
    "m05_audio": "m05_audio.omni.md",
    "m06_docx": "m06_docx.omni.md",
    "m07_pptx": "m07_pptx.omni.md",
    "m08_jpg_ocr": "m08_jpg_ocr.omni.md",
    "m09_huge1000p": "m09_huge1000p.omni.md",
    "m10_truncated": "m10_truncated.omni.md",
    "m11_ocr_spacing": "m11_ocr_spacing.omni.md",
}

# 三格式矩阵用的中间件 JSON 文件名
MULTI_NAMES = {
    "m01_etf_xlsx": "_t_M01_etf_xlsx_gov",
    "m02_bond_pdf": "_t_M02_bond_pdf_finance",
    "m03_report_pdf": "_t_M03_report_pdf_legal",
    "m04_html": "_t_M04_html_academic",
    "m04_html_quote": "_t_M04_html_academic_quote",
    "m05_audio": "_t_M05_audio_default",
    "m06_docx": "_t_M06_docx_custom_profile",
    "m07_pptx": "_t_M07_pptx_default",
    "m08_jpg_ocr": "_t_M08_jpg_ocr_strip",
    "m09_huge1000p": "_t_M09_huge1000p_gov",
    "m10_truncated": "_t_M10_truncated_default",
    "edge": "_t_M11_edge_all_flags",
    "edge_no": "_t_M12_edge_default_noStrip",
}


def wrap_json(markdown: str) -> str:
    data = {"markdown": markdown, "grounding": None, "outline": None,
            "source": "synthetic-fixture", "detail": "text"}
    return json.dumps(data, ensure_ascii=False)


def main():
    FIX.mkdir(parents=True, exist_ok=True)
    written = []
    # docx 矩阵：10 份合成 .omni.md
    for key, name in DOCX_NAMES.items():
        (FIX / name).write_text(DOCS[key], encoding="utf-8")
        written.append(name)
    # 三格式矩阵：13 份合成中间件 JSON
    multi_sources = dict(DOCS)
    multi_sources["m04_html_quote"] = D4Q_HTML
    edge = (FIX / "edge_case.md").read_text(encoding="utf-8")
    multi_sources["edge"] = edge
    multi_sources["edge_no"] = edge
    for key, name in MULTI_NAMES.items():
        (FIX / (name + ".json")).write_text(wrap_json(multi_sources[key]),
                                            encoding="utf-8")
        written.append(name + ".json")
    print("生成 %d 个 fixture：" % len(written))
    for w in sorted(written):
        print("  ", w)


if __name__ == "__main__":
    main()
