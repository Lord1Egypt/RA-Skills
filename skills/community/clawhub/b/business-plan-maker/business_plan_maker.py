#!/usr/bin/env python3
"""商业计划生成器 - 输入产品描述，自动生成完整商业计划书"""

import argparse
import json
import os
import sys
import textwrap
from datetime import datetime


# ── 快速模式模板 ──────────────────────────────────────────────────

def _quick_plan(product_desc: str) -> str:
    """生成基于模板的商业计划框架（不调用 API）"""
    today = datetime.now().strftime("%Y年%m月%d日")
    return textwrap.dedent(f"""\
        # 商业计划书

        **生成日期**: {today}
        **产品/业务**: {product_desc}

        ---

        ## 1. 执行摘要

        ### 项目概述
        {product_desc}

        ### 核心价值主张
        - 解决什么问题：[请在此填写目标用户的核心痛点]
        - 提供什么价值：[请在此填写解决方案的核心价值]
        - 目标用户：[请在此填写主要用户群体]

        ### 关键指标（预估）
        - 市场规模（TAM）：[请填写总可用市场]
        - 可服务市场（SAM）：[请填写可服务市场]
        - 可获得市场（SOM）：[请填写可获得市场]
        - 目标月收入（3年内）：[请填写预期月收入]

        ---

        ## 2. 市场分析

        ### 行业背景
        [请在此填写行业现状与趋势分析]

        ### 目标用户画像
        - 年龄：[ ]
        - 职业：[ ]
        - 痛点：[ ]
        - 付费意愿：[高/中/低]

        ### 市场规模
        - 全球市场：[ ]亿元
        - 国内市场：[ ]亿元
        - 年增长率：[ ]%

        ---

        ## 3. 竞争定位

        ### 竞争对手分析

        | 竞品 | 优势 | 劣势 | 定价 |
        |------|------|------|------|
        | 竞品A | | | |
        | 竞品B | | | |

        ### 差异化优势
        1. [请填写你的核心差异化优势]
        2. [请填写第二个差异化优势]
        3. [请填写第三个差异化优势]

        ### 市场定位
        [请描述你的定位——例如：性价比之王 / 高端专业 / 垂直细分龙头]

        ---

        ## 4. 收入模型

        ### 收入来源
        - [ ] 订阅制（月/年）
        - [ ] 一次性付费
        - [ ] 免费增值（Freemium）
        - [ ] 广告收入
        - [ ] 佣金/抽成
        - [ ] 增值服务

        ### 定价策略
        [请描述定价逻辑和价格梯度]

        ### 收入预测（首年）
        | 月份 | 预计用户数 | 预计收入 |
        |------|-----------|---------|
        | 第1月 | |
        | 第3月 | |
        | 第6月 | |
        | 第12月 | |

        ---

        ## 5. 运营计划

        ### 关键里程碑
        | 时间 | 里程碑 |
        |------|--------|
        | 第1月 | |
        | 第3月 | |
        | 第6月 | |
        | 第12月 | |

        ### 营销渠道
        - [ ] 社交媒体
        - [ ] 内容营销
        - [ ] SEO
        - [ ] 付费广告
        - [ ] 合作推广
        - [ ] 口碑传播

        ### 团队需求
        - 创始人：[ ]
        - 核心成员：[ ]
        - 外包/兼职：[ ]

        ---

        ## 6. 财务预测

        ### 启动成本
        | 项目 | 金额（元） |
        |------|-----------|
        | 开发成本 | |
        | 营销费用 | |
        | 运营成本 | |
        | 人员成本 | |
        | 其他 | |
        | **合计** | |

        ### 收支平衡预测
        - 预期收支平衡时间：第 [ ] 个月
        - 累计投入：¥[ ]
        - 累计收入：¥[ ]

        ### 融资需求（如有）
        - 融资轮次：[天使/Pre-A/A轮]
        - 融资金额：¥[ ]
        - 出让股份：[ ]%
        - 资金用途：
          - 产品开发：[ ]%
          - 市场营销：[ ]%
          - 团队扩张：[ ]%
          - 运营储备：[ ]%

        ---

        ## 7. 风险评估

        ### 主要风险
        | 风险 | 概率 | 影响 | 应对策略 |
        |------|------|------|---------|
        | 市场竞争激烈 | 高/中/低 | 高/中/低 | [请填写] |
        | 技术壁垒 | 高/中/低 | 高/中/低 | [请填写] |
        | 现金流不足 | 高/中/低 | 高/中/低 | [请填写] |
        | 政策风险 | 高/中/低 | 高/中/低 | [请填写] |

        ### 退出策略
        - [ ] 被收购
        - [ ] 持续运营 / 现金流
        - [ ] 上市（长线）

        ---

        *此文件由 Business Plan Maker 快速模式生成，内容为模板框架，需手动完善。*
        *使用 --mode full 可调用 AI 生成完整内容。*
    """)


# ── AI 完整模式 ──────────────────────────────────────────────────

def _call_llm(prompt: str, model: str | None = None) -> str:
    """调用 OpenAI API 生成内容"""
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("错误: 需要安装 openai 库。运行: pip install openai")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit("错误: 请设置环境变量 OPENAI_API_KEY")

    model_name = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位专业的商业计划书撰写专家。你擅长根据产品或业务描述，"
                    "生成结构完整、数据合理、具有说服力的商业计划书。"
                    "你的输出语言应与用户输入语言一致。"
                    "输出格式为 Markdown。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    return resp.choices[0].message.content or ""


def _full_plan(product_desc: str) -> str:
    """调用 AI 生成完整商业计划书"""
    prompt = textwrap.dedent(f"""\
        请根据以下产品/业务描述，生成一份完整的商业计划书。

        产品/业务描述：{product_desc}

        请包含以下章节：
        1. 执行摘要 —— 简洁有力地概述项目、价值主张和目标
        2. 市场分析 —— 行业背景、目标用户画像、市场规模（TAM/SAM/SOM）
        3. 竞争定位 —— 竞争对手分析、差异化优势、市场定位
        4. 收入模型 —— 收入来源、定价策略、收入预测
        5. 运营计划 —— 关键里程碑、营销渠道、团队需求
        6. 财务预测 —— 启动成本、收支平衡分析、融资需求（如适用）
        7. 风险评估 —— 主要风险与应对策略、退出策略

        要求：
        - 输出语言：{_detect_lang(product_desc)}
        - 格式为 Markdown
        - 数据尽量合理且有据可依
        - 直接写商业计划书内容，不要额外解释
    """)
    return _call_llm(prompt)


def _detect_lang(text: str) -> str:
    """简单检测文本语言"""
    for ch in text[:200]:
        if '\u4e00' <= ch <= '\u9fff':
            return "中文"
    return "与用户输入相同的语言"


# ── 主入口 ───────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="商业计划生成器 — 输入产品描述，自动生成商业计划书",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            示例:
              %(prog)s --mode full "AI驱动的健身App"
              %(prog)s --mode quick "在线教育平台"
              %(prog)s --output plan.md --mode full "SaaS工具"
        """),
    )
    parser.add_argument(
        "description",
        type=str,
        help="产品/业务描述",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "quick"],
        default="full",
        help="生成模式: full=AI生成(默认), quick=模板框架(无需API)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="输出文件路径（默认打印到终端）",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default=None,
        help="输出语言（默认自动检测）",
    )

    args = parser.parse_args()

    if args.mode == "quick":
        plan = _quick_plan(args.description)
    else:
        print("正在调用 AI 生成商业计划书...", file=sys.stderr)
        plan = _full_plan(args.description)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"已保存至: {args.output}", file=sys.stderr)
    else:
        print(plan)


if __name__ == "__main__":
    main()
