---
name: ai-eval-toolkit
slug: ai-eval-toolkit
display_name: LLM评测工具链
displayName: LLM评测工具链
title: LLM评测工具链
version: 1.0.0
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: LLM 评测工具链（可运行实现）——把评测方法论变成能直接跑的本地引擎：评测集管理（JSONL 建集/质量检查/规模统计）、幻觉检测引擎（数字一致性/引用校验/否定矛盾/关键论断互证四类规则检测）、RAG 指标计算（RAGAS 四指标的本地简化实现：忠实度/答案相关性/上下文精度/上下文召回）、回归对比（基线 vs 新结果差异判定）、报告生成与上线门禁（分场景得分/门禁判定/报告输出）。零依赖纯标准库，本地闭环不联网。与「LLM 质量评测」（方法论）互补——那个讲怎么做，这个给能跑的实现。面向 AI 工程师、测试与质量负责人。
description_en: A runnable LLM evaluation toolkit — turning evaluation methodology into a local engine you can actually execute. Covers evaluation-set management (JSONL creation, quality checks, size statistics), a hallucination detection engine (four rule-based detectors, numeric consistency, citation validation, negation contradiction, key-claim cross-checking), RAG metric computation (local simplified implementation of the RAGAS metrics, faithfulness, answer relevance, context precision, context recall), regression comparison (baseline versus new-result difference judgment), and report generation with launch gates (per-scenario scores, gate decisions, report output). Zero-dependency, pure standard library, local and offline. Complements the LLM quality evaluation playbook (methodology); this toolkit provides the runnable implementation. Built for AI engineers, QA and quality leads.
tags:
  - LLM评测
  - 评测工具
  - 幻觉检测
  - RAG评测
  - RAGAS
  - 回归测试
  - 评测集
  - Eval Toolkit
  - LLM Evaluation
  - Hallucination
  - 质量门禁
  - 本地工具
---

# LLM 评测工具链

能直接跑的 LLM 评测引擎：**建评测集、测幻觉、算 RAG 指标、对比回归、出报告卡门禁**。与「LLM 质量评测」skill（方法论）配套——那个讲"怎么做"，这个给"能跑的实现"。

## 什么时候用这个技能

- **建评测集**：「评测集怎么建？帮我生成 JSONL 模板？」
- **测幻觉**：「这批回答里有没有幻觉？」
- **算 RAG 指标**：「RAG 系统忠实度/召回怎么算？」
- **回归对比**：「新 Prompt/模型比基线好还是差？」
- **卡门禁**：「质量达标了吗？能上线吗？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「评测集 JSONL 格式怎么组织？」
> 「怎么检测回答里的幻觉？」
> 「RAG 四指标本地怎么算？」

### 模式二：本地工具（可运行引擎）

```bash
# ① 评测集管理：初始化/质量检查/规模统计
python tools/eval_toolkit.py dataset --action init --out evalset.jsonl
python tools/eval_toolkit.py dataset --action check --file evalset.jsonl
python tools/eval_toolkit.py dataset --action stat --file evalset.jsonl

# ② 幻觉检测：对回答跑四类规则检测
python tools/eval_toolkit.py hallucination --answer "该产品2025年销量100万台" --source "2026年报告显示销量50万台"

# ③ RAG 指标计算（RAGAS 简化实现）
python tools/eval_toolkit.py ragscore --answer "..." --context "..." --question "..."

# ④ 回归对比：基线 vs 新结果
python tools/eval_toolkit.py compare --base baseline.json --new result.json

# ⑤ 报告与门禁
python tools/eval_toolkit.py report --result result.json --gate 0.05

# 查看全部命令
python tools/eval_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 工具链全景 | `references/01-工具链全景.md` | 五个引擎、数据流、与方法论 skill 的关系 |
| ② 评测集管理 | `references/02-评测集管理.md` | JSONL 格式、字段规范、质量检查 |
| ③ 幻觉检测引擎 | `references/03-幻觉检测引擎.md` | 四类规则检测器原理与局限 |
| ④ RAG 指标计算 | `references/04-RAG指标计算.md` | RAGAS 简化实现原理与口径 |
| ⑤ 回归对比 | `references/05-回归对比.md` | 基线管理、差异判定、防假回归 |
| ⑥ 报告与门禁 | `references/06-报告与门禁.md` | 报告结构、门禁规则、与 CI 集成 |
| ⑦ 与平台工具衔接 | `references/07-与平台工具衔接.md` | RAGAS/OpenAI Evals/LangSmith 对比与升级路径 |
| ⑧ FAQ | `references/08-FAQ.md` | 高频疑问 |

## 快速上手（三步）

1. **建集**：`dataset init` 出 JSONL 模板，02 模块看字段规范；
2. **测质量**：`hallucination`/`ragscore` 跑检测与指标，03-04 模块看原理；
3. **卡门禁**：`compare`/`report` 出对比与门禁，05-06 模块看规则。

## 能力边界（如实说明）

- **规则检测不是完美检测**：本工具链的幻觉/RAG 指标是规则与启发式实现（零依赖），准确率不及 RAGAS/评估器等专业框架——适合快速基线、CI 门禁与教学演示；生产高要求场景按 07 模块升级到专业框架；
- **不调外部模型**：LLM-as-Judge 类指标需自行接入 API（本工具提供接口规范，不内置调用）；
- **工具纯本地**：不联网、不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：这个工具链和 LLM 质量评测 skill 什么关系？** 方法论 vs 实现：那个讲指标怎么选、评测集怎么建（方法论），这个给能跑的代码（评测集管理/幻觉检测/RAG 指标/回归门禁）。配套使用。
- **Q：规则检测靠谱吗？** 适合快速基线（检出率高、误报偏高需人工复核）；高要求场景升级 RAGAS 等专业框架（07 模块给了对照与路径）。
- **Q：评测集格式是什么？** JSONL，每行一个用例：question/answer/context/reference/gold 等字段（02 模块有模板）。
- **Q：工具脚本要装依赖吗？** 不需要，纯 Python 标准库，开箱即跑。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 LLM 评测工具实现、算法逻辑与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与安全保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。
