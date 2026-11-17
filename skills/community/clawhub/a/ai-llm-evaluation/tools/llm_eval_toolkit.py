# -*- coding: utf-8 -*-
"""LLM 质量评测 - 本地工具（零依赖，Python 标准库）

命令：
  metrics   指标速查（按场景输出评测指标建议）
  setdesign 评测集设计清单（按类型）
  rag       RAG 评测指标说明（RAGAS 四指标）
  compare   模型对比矩阵
  report    评测报告模板
"""
import argparse
import sys

# ---------------- 场景指标库 ----------------
SCENE_METRICS = {
    "rag": [
        ("忠实度 Faithfulness", "回答是否忠于检索上下文（RAG 核心指标）"),
        ("答案相关性 Answer Relevance", "回答是否切题"),
        ("上下文召回 Context Recall", "关键信息是否被召回（检索端）"),
        ("上下文精度 Context Precision", "召回片段是否相关（检索端）"),
    ],
    "qa": [
        ("正确率/准确率", "有标准答案时"),
        ("答案相关性", "开放问答"),
        ("幻觉率", "含虚构/矛盾回答占比"),
        ("拒绝率", "知识外问题得体拒绝比例"),
    ],
    "summary": [
        ("忠实度", "摘要是否忠于原文"),
        ("信息覆盖", "关键信息保留比例"),
        ("冗余度", "冗余信息占比"),
    ],
    "classification": [
        ("准确率/精确率/召回率/F1", "结构化任务核心指标"),
        ("错误分析", "混淆矩阵定位问题类别"),
    ],
    "code": [
        ("通过率", "生成代码通过测试比例"),
        ("代码质量", "Review 评分/复杂度"),
        ("安全性", "漏洞扫描结果"),
    ],
    "writing": [
        ("指令遵循", "是否符合写作要求"),
        ("风格一致性", "与目标风格匹配度"),
        ("人工评分", "内容质量与创意"),
    ],
    "translation": [
        ("BLEU/COMET", "自动翻译质量"),
        ("术语一致性", "专业术语是否统一"),
        ("人工评分", "流畅度与准确度"),
    ],
}

# ---------------- 评测集类型清单 ----------------
SETDESIGN = {
    "qa": [
        "黄金数据集：常见高频问题 30-50 条，人工标注标准答案",
        "边界用例：超长输入、空输入、单字输入",
        "文档外用例：知识边界外问题（测拒绝）",
        "对抗用例：指令改写、噪声输入、角色混淆",
        "规模建议：起步 50-100 条，生产 500+",
    ],
    "rag": [
        "标准问答：答案明确在文档中（忠实度基线）",
        "跨文档问答：需融合多篇文档（召回完整度）",
        "文档外问题：答案不在知识库（防硬答）",
        "相似内容陷阱：多个相似文档（防张冠李戴）",
        "长文档深挖：答案在文档深处（检索深度）",
        "时效性问题：知识库更新后（防旧版污染）",
    ],
    "classification": [
        "类别覆盖：每个类别至少 10-20 条",
        "边界样本：难以分类的样本（核心价值）",
        "类别不平衡测试：验证少数类表现",
        "对抗样本：近似其他类别的陷阱输入",
    ],
    "code": [
        "功能用例：标准功能请求",
        "边界用例：空输入、超长输入、异常参数",
        "安全用例：注入/越权（衔接红队）",
        "重构用例：既有代码上做修改",
    ],
}

# ---------------- RAG 四指标 ----------------
RAG_METRICS = [
    ("忠实度 Faithfulness", "回答中的论断是否都能在检索上下文中找到依据", "生成端核心"),
    ("答案相关性 Answer Relevance", "回答是否直接切题，不评价正确性", "生成端"),
    ("上下文精度 Context Precision", "召回的检索片段有多大比例是相关的、必要的", "检索端"),
    ("上下文召回 Context Recall", "黄金答案依据的信息是否都被检索召回", "检索端"),
]

# ---------------- 对比维度 ----------------
COMPARE_DIMS = [
    ("质量", "用同一评测集跑核心指标（忠实度/准确率等）"),
    ("效率", "延迟（TTFT/TPS）与吞吐"),
    ("成本", "单次调用成本与月成本估算（含输入输出 Token）"),
    ("稳定性", "多轮输出方差（一致性）"),
    ("安全", "拒绝率、有害输出率（衔接红队）"),
    ("合规", "数据用途条款、部署地、数据出境约束"),
]

# ---------------- 报告模板 ----------------
REPORT_TEMPLATE = """评测报告模板（核心结构）

一、评测概况
- 评测时间：____
- 评测集版本：____（规模：__条，含对抗__条）
- 被测版本：模型____ / Prompt____ / 知识库____
- 评估器：____（人工抽样复核率：__%）

二、总览
- 综合得分：__（基线：__，变化 ↑/↓/持平）
- 门禁结论：通过 / 拦截

三、分场景得分（对比基线，退化项标红）
| 场景 | 指标 | 得分 | 基线 | 变化 |
| 客服问答 | 忠实度 | __ | __ | __ |
| ... |

四、问题样本（Top 失败案例）
| # | 输入 | 输出 | 问题类型 | 严重度 |

五、趋势（可选）
- 近 N 次评测得分曲线：__

六、结论与建议
- 通过 / 回滚 / 修复项清单：____
"""


def cmd_metrics(args):
    if args.scene not in SCENE_METRICS:
        print("错误：--scene 仅支持 rag / qa / summary / classification / code / writing / translation。")
        return 2
    print("=" * 60)
    print(f"场景：{args.scene}　评测指标建议：")
    for i, (name, detail) in enumerate(SCENE_METRICS[args.scene], 1):
        print(f"{i}. {name}：{detail}")
    return 0


def cmd_setdesign(args):
    if args.type not in SETDESIGN:
        print("错误：--type 仅支持 qa / rag / classification / code。")
        return 2
    print("=" * 60)
    print(f"类型：{args.type}　评测集设计清单：")
    for i, item in enumerate(SETDESIGN[args.type], 1):
        print(f"{i}. {item}")
    return 0


def cmd_rag(args):
    print("=" * 60)
    print("RAG 评测指标（RAGAS 四指标）：")
    for i, (name, detail, side) in enumerate(RAG_METRICS, 1):
        print(f"{i}. {name}：{detail}　[{side}]")
    print()
    print("诊断顺序：先查检索端（召回/精度），再查生成端（忠实度/相关性）")
    return 0


def cmd_compare(args):
    print("=" * 60)
    print("模型对比矩阵（同一评测集对比）：")
    for i, (dim, detail) in enumerate(COMPARE_DIMS, 1):
        print(f"{i}. {dim}：{detail}")
    print()
    print("流程：同集跑分 → 成本质量权衡 → 灰度 A-B（10% 分流 1-2 周）→ 上线决策")
    return 0


def cmd_report(args):
    print("=" * 60)
    print("评测报告模板：")
    print(REPORT_TEMPLATE)
    return 0


def main():
    p = argparse.ArgumentParser(description="LLM 质量评测本地工具（零依赖）")
    sub = p.add_subparsers(dest="cmd")

    p_metrics = sub.add_parser("metrics", help="指标速查")
    p_metrics.add_argument("--scene", required=True,
                           choices=["rag", "qa", "summary", "classification", "code", "writing", "translation"])

    p_set = sub.add_parser("setdesign", help="评测集设计清单")
    p_set.add_argument("--type", required=True, choices=["qa", "rag", "classification", "code"])

    sub.add_parser("rag", help="RAG 评测指标说明")
    sub.add_parser("compare", help="模型对比矩阵")
    sub.add_parser("report", help="评测报告模板")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return 0
    fn = {"metrics": cmd_metrics, "setdesign": cmd_setdesign,
          "rag": cmd_rag, "compare": cmd_compare, "report": cmd_report}[args.cmd]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
