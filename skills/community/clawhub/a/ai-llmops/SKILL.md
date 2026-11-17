---
name: ai-llmops
slug: ai-llmops
display_name: AI模型资产管理
displayName: AI模型资产管理
title: AI模型资产管理
version: 1.0.0
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: AI 模型与资产全生命周期管理（LLMOps）实操手册——从"有模型在用"到"资产清清楚楚"：资产全景与台账（模型/Prompt/知识库/评估集/Agent 配置五类资产登记）、模型卡与注册（Model Card 字段规范、注册流程、元数据管理）、版本管理（模型/Prompt/知识库版本化、灰度发布、一键回滚）、上线下线管理（上线审批、退役下线、废弃处置与迁移）、漂移监控（数据漂移/概念漂移/模型漂移、监控指标与告警阈值）、成本治理（Token 成本核算、预算控制、路由分层、蒸馏与缓存降本）、治理制度与流程（角色职责、审批流、审计留痕）。附零依赖本地工具一键出盘点清单、模型卡模板、生命周期检查、漂移监控要点与成本治理清单。面向 AI 平台、工程、运维与财务负责人——与企业 AI 治理（管制度）互补，本技能管资产与工程。
description_en: A hands-on playbook for AI model and asset lifecycle management (LLMOps) — from "we have models in use" to crystal-clear asset governance. Covers asset inventory (five asset types, models, prompts, knowledge bases, evaluation sets, agent configurations), model cards and registration (Model Card fields, registration workflow, metadata), version management (model/prompt/knowledge-base versioning, canary releases, one-click rollback), launch and retirement (approval gates, decommissioning, migration), drift monitoring (data drift, concept drift, model drift, metrics and alert thresholds), cost governance (token cost accounting, budgets, routing tiers, distillation and caching), and governance processes (roles, approval flows, audit trails). Includes a zero-dependency local toolkit for inventory checklists, model card templates, lifecycle checks, drift monitoring points and cost governance lists. Built for AI platform, engineering, operations and finance leaders — complements enterprise AI governance (which manages policy); this skill manages assets and engineering.
tags:
  - LLMOps
  - 模型管理
  - AI资产管理
  - 模型卡
  - 版本管理
  - 漂移监控
  - 成本治理
  - Model Card
  - MLOps
  - Model Governance
  - FinOps
  - AI运维
---

# AI 模型资产管理（LLMOps）

AI 资产的全生命周期"管家"：**建台账、管版本、控上线、盯漂移、算成本**。当企业用上多个模型、多套 Prompt、多个知识库，没有资产管理就会出现"谁在用哪个模型都不知道、成本失控、更新了没人知道"。

## 什么时候用这个技能

- **建台账**：「我们的 AI 资产有哪些？都登记了吗？」
- **管版本**：「模型/Prompt 升级怎么管理？出问题怎么回滚？」
- **控上线**：「新模型上线要什么流程？旧模型怎么退役？」
- **盯漂移**：「模型效果变差了怎么发现？」
- **算成本**：「AI 调用成本怎么核算和控制？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「怎么建 AI 资产台账？」
> 「模型升级后怎么回滚？」
> 「AI 成本失控了怎么治理？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 资产盘点：输出 AI 资产盘点清单
python tools/llmops_toolkit.py inventory

# ② 模型卡模板
python tools/llmops_toolkit.py modelcard

# ③ 生命周期检查（按阶段）
python tools/llmops_toolkit.py lifecycle --phase launch   # register/launch/monitor/retire

# ④ 漂移监控要点
python tools/llmops_toolkit.py drift

# ⑤ 成本治理清单
python tools/llmops_toolkit.py cost

# 查看全部命令
python tools/llmops_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 资产全景与台账 | `references/01-资产全景与台账.md` | 五类 AI 资产、台账字段、盘点流程 |
| ② 模型卡与注册 | `references/02-模型卡与注册.md` | Model Card 规范、注册流程、元数据 |
| ③ 版本管理 | `references/03-版本管理.md` | 模型/Prompt/知识库版本化、灰度、回滚 |
| ④ 上线下线管理 | `references/04-上线下线管理.md` | 上线审批、退役下线、废弃处置 |
| ⑤ 漂移监控 | `references/05-漂移监控.md` | 三类漂移、监控指标、告警阈值 |
| ⑥ 成本治理 | `references/06-成本治理.md` | Token 成本核算、预算、路由降本 |
| ⑦ 治理制度与流程 | `references/07-治理制度与流程.md` | 角色职责、审批流、审计留痕 |
| ⑧ FAQ | `references/08-FAQ.md` | 高频疑问 |

## 快速上手（三步）

1. **建台账**：`inventory` 出盘点清单，01 模块看资产分类；
2. **管版本**：`modelcard`/`lifecycle` 出模板与检查，02-04 模块看流程；
3. **盯运行**：`drift`/`cost` 出监控与成本要点，05-06 模块看指标。

## 能力边界（如实说明）

- **本技能是资产管理方法论与流程框架，不是资产管理平台**：台账/版本/监控需落到现有工具链（MLflow、LangSmith、内部平台等）实施；
- **指标阈值是经验值**：漂移阈值、成本预算需按业务规模校准；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：资产台账要管什么？** 五类：模型、Prompt、知识库、评估集、Agent 配置——每类登记"版本+负责人+状态+依赖"（见 01 模块）。
- **Q：模型升级出问题怎么回滚？** 版本管理先行：每版固化（模型+Prompt+知识库快照），发布走灰度，异常一键回退到上一可用版本（见 03 模块）。
- **Q：怎么发现模型变差？** 漂移监控：线上指标（拒绝率/满意度）+ 定期评测（评测集回归）+ 数据漂移检测三轨（见 05 模块）。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 LLMOps 资产管理方法论、流程与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与安全保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。
