---
name: ai-llm-evaluation
slug: ai-llm-evaluation
display_name: LLM质量评测
displayName: LLM质量评测
title: LLM质量评测
version: 1.0.0
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: LLM 应用质量评测与回归测试实操手册——从"感觉不错"到"可度量可门禁"：评测全景与指标体系（正确性/相关性/忠实度/幻觉率/鲁棒性/效率）、评测集构建（黄金数据集/对抗样本/领域评测集/规模估算）、RAG 系统评测（RAGAS 四指标：忠实度/答案相关性/上下文精度/上下文召回）、幻觉检测与度量（事实性幻觉/提示幻觉/上下文矛盾分类与检测方法）、Prompt 回归测试（用例管理/回归门禁/漂移检测/版本对比）、模型对比选型（评测矩阵/成本质量权衡/多模型 A-B/上线决策）、评测流水线与报告（自动化评测/评分聚合/报告模板/上线门禁）。附零依赖本地工具一键查指标、建评测集清单、看 RAG 指标、出对比矩阵、生成评测报告模板。面向 AI 工程师、测试、产品与质量负责人——与 AI 安全红队测试（测安全）互补，本技能测质量。
description_en: A hands-on playbook for LLM application quality evaluation and regression testing — from "feels fine" to measurable and gated. Covers the evaluation landscape and metric system (correctness, relevance, faithfulness, hallucination rate, robustness, efficiency), test-set construction (golden datasets, adversarial samples, domain test sets, size estimation), RAG evaluation (RAGAS metrics, faithfulness, answer relevance, context precision, context recall), hallucination detection and measurement (factual, prompt, context-contradiction taxonomy), prompt regression testing (case management, regression gates, drift detection, version comparison), model comparison and selection (evaluation matrix, cost-quality trade-off, A-B testing, go-live decisions), and evaluation pipelines with reporting (automated evaluation, score aggregation, report templates, launch gates). Includes a zero-dependency local toolkit for metric lookups, test-set checklists, RAG metrics, comparison matrices and report templates. Built for AI engineers, QA, product and quality leaders — complements the AI security red-team skill (which tests safety); this skill tests quality.
tags:
  - LLM评测
  - 模型评估
  - RAG评测
  - 幻觉检测
  - Prompt测试
  - 回归测试
  - 质量门禁
  - LLM Evaluation
  - RAGAS
  - Model Eval
  - 测试集
  - AI质量
---

# LLM 质量评测

AI 应用质量的"度量衡与门禁"：**定指标、建评测集、跑评测、出报告、卡上线**。当"AI 回答好不好"不能靠感觉，就需要一套可复现、可度量、可门禁的评测体系——本技能就是这套体系。

## 什么时候用这个技能

- **建评测体系**：「我们 AI 应用怎么评估质量？用什么指标？」
- **建评测集**：「评测用例怎么设计？要多少条？」
- **RAG 评测**：「知识库问答系统效果怎么测？」
- **幻觉度量**：「怎么发现和量化幻觉？」
- **回归门禁**：「Prompt/模型更新后怎么防止质量回退？」
- **选型决策**：「换模型/换版本怎么比？怎么决定上线？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「我们的客服 AI 怎么建评测体系？」
> 「RAG 系统该测哪些指标？」
> 「模型更新后怎么防止质量回退？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 指标速查：按场景输出评测指标建议
python tools/llm_eval_toolkit.py metrics --scene rag

# ② 评测集设计：按类型输出评测集构建清单
python tools/llm_eval_toolkit.py setdesign --type qa

# ③ RAG 指标说明
python tools/llm_eval_toolkit.py rag

# ④ 模型对比矩阵
python tools/llm_eval_toolkit.py compare

# ⑤ 评测报告模板
python tools/llm_eval_toolkit.py report

# 查看全部命令
python tools/llm_eval_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 评测全景与指标 | `references/01-评测全景与指标.md` | 评测金字塔、核心指标定义与选择 |
| ② 评测集构建 | `references/02-评测集构建.md` | 黄金数据集、对抗样本、规模估算 |
| ③ RAG 系统评测 | `references/03-RAG系统评测.md` | RAGAS 四指标、知识库问答评测 |
| ④ 幻觉检测与度量 | `references/04-幻觉检测与度量.md` | 幻觉分类、检测方法、量化指标 |
| ⑤ Prompt 回归测试 | `references/05-Prompt回归测试.md` | 用例管理、回归门禁、漂移检测 |
| ⑥ 模型对比选型 | `references/06-模型对比选型.md` | 评测矩阵、成本质量权衡、上线决策 |
| ⑦ 评测流程与报告 | `references/07-评测流程与报告.md` | 评测流水线、评分聚合、报告模板 |
| ⑧ FAQ | `references/08-FAQ.md` | 高频疑问 |

## 快速上手（三步）

1. **定指标**：`metrics` 命令按场景查指标，01 模块看指标详解；
2. **建评测集**：`setdesign` 按类型出清单，02/03 模块看设计方法；
3. **跑评测出报告**：`rag`/`compare`/`report` 出结构化结果，07 模块看流水线。

## 能力边界（如实说明）

- **本技能是评测方法论与工具框架，不是评测执行器**：指标计算需接入具体模型/评测框架（如 RAGAS、OpenAI Evals、LangSmith 等）执行；
- **指标口径因场景而异**：评测集质量决定评测可信度，本技能提供设计方法而非万能指标；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：评测集要多少条用例？** 起步 50-100 条覆盖核心场景，生产级建议 500+ 且含对抗样本（见 02 模块）。
- **Q：RAG 系统最该测什么？** 忠实度与上下文召回优先——回答是否忠于检索内容、关键信息是否被召回（见 03 模块）。
- **Q：幻觉能量化吗？** 可以：幻觉率 = 含幻觉回答数 / 总回答数，配合事实性检测与人工抽样双轨（见 04 模块）。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 LLM 评测方法论、指标体系、流程与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与安全保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。
