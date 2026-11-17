---
name: data-element-dx-skillkit
description: 数据要素 × 国企/传统集团数字化转型端到端交付技能套件（7 技能）。当用户要"数据要素转型/国企数字化/数据资产入表/数据资产盘点/DCMM评估/数据治理方案/数据产品设计/数字化转型整体交付"或整套交付时使用。入口技能，负责路由到 dx-* 子技能。
description_en: End-to-end skill kit (7 skills) for the data-element transformation of Chinese SOEs and traditional conglomerates. Use as the entry point when the user wants a full digital-transformation delivery, data-asset capitalization (入表), DCMM assessment, data-governance scheme, or data-product design. Routes to the dx-* sub-skills.
license: Apache-2.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
metadata:
  author: 大数据猎人
  version: "2.0.1"
  domain: 数据要素×国企数字化转型·套件入口
  skills: ["dx-engagement-orchestrator", "dx-data-baseline", "dx-data-quality", "dx-application-plan", "dx-architecture-opt", "dx-competitor-scout", "dx-industry-research"]
---

# 数据要素 × 国企数字化转型 · 端到端交付技能套件（入口）

本文件是整个 **data-element-dx-skillkit** 的入口与路由文档。安装本套件后，**7 个子技能与 `_shared` 共享资源位于本入口同级目录**，相对引用（`../_shared/...`）在安装后依然有效。

## 何时使用

- 用户提出**整套**交付需求："数据要素转型""国企数字化""数据资产入表""数字化转型方案/汇报"。
- 用户需求**跨多个环节**（如"盘点完直接给治理方案"），需要编排而非单点解答。
- 不确定该用哪个子技能时，先读本入口做路由。

**单点需求不需要本入口**，直接进入对应子技能（见下表）。

## 套件结构（7 技能 + 共享资源）

| 子技能 | 覆盖环节 | 典型触发 |
|---|---|---|
| `dx-engagement-orchestrator` | **编排层**：端到端交付计划、门禁、口径一致性 | "完整做一遍""先出交付计划" |
| `dx-data-baseline` | 数据现状摸底 / 资产盘点 / DCMM 初评 | "盘一下我们有什么数据""数据目录" |
| `dx-data-quality` | 数据质量评估 / 治理方案 | "数据质量怎么样""脏数据太多" |
| `dx-application-plan` | 应用场景地图 / 数据产品设计 / 入表路径 | "数据能做什么""数据产品""入表" |
| `dx-architecture-opt` | 数据架构优化 / 平台选型 | "架构怎么改""要不要上湖仓" |
| `dx-competitor-scout` | 竞品 / 同业动态情报 | "同行怎么做数据""对标XX" |
| `dx-industry-research` | 行业研究 / 政策解读 | "行业趋势""政策怎么看" |

共享资源（`_shared/`）：脚本（`gate_check.py` 门禁、`scan_assets.py` 资产扫描、`maturity_score.py` 成熟度）、模板、gotchas 维护规范、触发器测试集（`_shared/eval/trigger-eval.md`）。

## 使用流程

```
用户需求
├─ 跨环节/整套 → dx-engagement-orchestrator（编排：交付计划 → 门禁 → 口径一致性）
│      └─ 各阶段按需调用 dx-* 子技能，产出挂回编排
├─ 单环节     → 直接进入对应子技能（上表）
└─ 不确定     → 先按上表读 description 判断，仍不确定走编排层
```

## 关键约定

- **门禁**：每个交付物必须通过 `_shared/scripts/gate_check.py`（存在性 → 实质性 → 挂接性 → 一致性）。
- **口径**：多材料交付必须维护数字台账，跨材料比对（`gate_check.py` 一致性检查）。
- **Gotchas（仅主理人手工维护，Agent 不参与）**：试跑中的经验教训由项目主理人在复盘时**手工记录到 `CHANGELOG.md`**（静态文档）。Agent 的职责止步于在交付报告中提出改进建议，**不得以任何方式修改技能文档**。
- **虚构演示**：`_demo-run/` 与 README 中的"集团A/集团B"为完全虚构案例，非真实客户数据。
