---
name: ai-observability
slug: ai-observability
display_name: AI可观测性监控
displayName: AI可观测性监控
title: AI可观测性监控
version: 1.0.0
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: AI 应用可观测性与生产监控实操手册——AI 进生产后的"仪表盘与探照灯"：可观测性全景（三大支柱：日志/指标/追踪 + AI 特有观测对象）、调用追踪与日志规范（LLM 调用追踪、Span 设计、会话级追踪、敏感信息过滤）、质量监控指标（幻觉率/拒答率/满意度/转人工率实时看板）、性能与成本监控（延迟/吞吐/Token 成本实时追踪）、护栏与安全监控（护栏命中率/注入检测/敏感数据泄漏监控）、告警体系（分级告警/阈值设计/通知路由/告警疲劳治理）、监控平台与落地（埋点规范/工具选型/灰度期监控）。附零依赖本地工具一键出三大支柱清单、监控指标表、告警设计、追踪规范与落地路线。面向 AI 平台、SRE、运维与质量负责人——与 LLM 评测（离线质量）互补，本技能管线上运行质量。
description_en: A hands-on playbook for AI application observability and production monitoring — the dashboard and searchlight once AI goes live. Covers the observability landscape (three pillars, logs, metrics and traces, plus AI-specific observation targets), call tracing and logging standards (LLM call traces, span design, session-level tracing, sensitive-information filtering), quality monitoring metrics (hallucination rate, refusal rate, satisfaction, human-handoff rate dashboards), performance and cost monitoring (latency, throughput, token cost in real time), guardrail and security monitoring (guardrail hit rate, injection detection, sensitive-data leakage), alerting (severity tiers, threshold design, routing, alert fatigue), and platform adoption (instrumentation standards, tooling selection, canary-period monitoring). Includes a zero-dependency local toolkit for pillar checklists, metric tables, alert design, tracing standards and adoption roadmaps. Built for AI platform, SRE, operations and quality leaders — complements LLM evaluation (offline quality); this skill governs runtime quality.
tags:
  - AI可观测性
  - LLM监控
  - 生产监控
  - 告警
  - 调用追踪
  - SRE
  - AI运维
  - Observability
  - LLM Monitoring
  - Tracing
  - Alerting
  - 幻觉监控
---

# AI 可观测性与生产监控

AI 应用生产运行的"仪表盘 + 探照灯"：**看得见、测得准、告得动、查得到**。当 AI 应用上线，传统监控不够用——要监控的不只是服务器，还有幻觉率、Token 成本、护栏命中这些 AI 特有的东西。

## 什么时候用这个技能

- **建监控**：「AI 应用上线后要监控什么？」
- **查问题**：「线上回答变差/报错/异常怎么定位？」
- **设告警**：「什么情况要告警？阈值怎么定？」
- **管成本**：「线上 Token 成本怎么实时盯？」
- **保安全**：「护栏命中率、注入攻击怎么监控？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

> 「AI 应用上线后要建哪些监控？」
> 「线上幻觉率怎么实时监控？」
> 「告警太多怎么办？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 三大支柱要点
python tools/observability_toolkit.py pillars

# ② 核心监控指标
python tools/observability_toolkit.py metrics

# ③ 告警设计（分级）
python tools/observability_toolkit.py alert

# ④ 调用追踪规范
python tools/observability_toolkit.py trace

# ⑤ 落地路线
python tools/observability_toolkit.py plan

# 查看全部命令
python tools/observability_toolkit.py --help
```

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 可观测性全景 | `references/01-可观测性全景.md` | 三大支柱、AI 特有观测对象 |
| ② 调用追踪与日志 | `references/02-调用追踪与日志.md` | Span 设计、会话追踪、敏感过滤 |
| ③ 质量监控指标 | `references/03-质量监控指标.md` | 幻觉率/拒答率/满意度/转人工看板 |
| ④ 性能与成本监控 | `references/04-性能与成本监控.md` | 延迟/吞吐/Token 成本实时追踪 |
| ⑤ 护栏与安全监控 | `references/05-护栏与安全监控.md` | 护栏命中/注入检测/数据泄漏 |
| ⑥ 告警体系 | `references/06-告警体系.md` | 分级告警、阈值、通知路由 |
| ⑦ 平台与落地 | `references/07-平台与落地.md` | 埋点规范、工具选型、灰度监控 |
| ⑧ FAQ | `references/08-FAQ.md` | 高频疑问 |

## 快速上手（三步）

1. **定范围**：`pillars` 出三大支柱要点，01 模块看全景；
2. **选指标**：`metrics` 出监控指标表，03-05 模块看详解；
3. **建告警**：`alert`/`trace`/`plan` 出设计与路线，06-07 模块看落地。

## 能力边界（如实说明）

- **本技能是监控方法论与设计框架，不是监控产品**：埋点/告警/看板需落到现有可观测性平台（Prometheus/Grafana、LangSmith、OpenTelemetry 等）实施；
- **指标与阈值是经验值**：需按业务规模与风险等级校准；
- **工具不联网**：本地规则匹配，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：AI 监控和普通应用监控有什么区别？** 普通监控看服务器/接口；AI 监控还要看幻觉率、Token 成本、护栏命中、Prompt 质量这些模型特有维度（见 01 模块）。
- **Q：幻觉率能实时监控吗？** 可以：自动检测（规则/评估器）覆盖大部分，配合抽样人工复核；对高危场景设实时告警（见 03 模块）。
- **Q：告警太多怎么办？** 分级治理：预警/告警/严重三级 + 阈值校准 + 聚合去重 + 值班轮转（见 06 模块）。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 AI 可观测性方法论、指标体系、流程与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与安全保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。
