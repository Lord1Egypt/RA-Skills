---
name: auto-coding-v3
description: "智能自主编码系统 v3.7.17-compliance — 全子代理架构 + 分阶段技能注入。支持 8 步循环、Reviewer 否决权、复杂度自动分级、Risk Scorecard 量化检测。触发词: auto-coding, Auto coding, 启动自动编码"
license: MIT
---

# Auto-Coding v3.7.17-compliance

## 概述 / Overview

Auto-Coding 是一个智能自主编码系统，通过全子代理架构 + 分阶段技能注入，完成从需求到代码的完整开发流程。

Auto-Coding is an intelligent autonomous coding system that completes the full development lifecycle from requirements to code through a fully sub-agent architecture with staged skill injection.

**本质**: 单进程串行 + 多角色 Prompt + 多模型切换。每一步换不同的人格和模型来审视代码，不是真正的多 Agent 并行。

**Essence**: Single-process serial execution + multi-role prompting + multi-model switching. Each step uses a different persona and model to review the code — not true multi-agent parallelism.

**核心特性**:
- 全子代理架构 — 主会话只做监工，所有干活用子代理执行
- 分阶段技能注入 — 每阶段注入对应技能文件，≤2 技能/阶段
- 8 步循环 — 设计→分解→编码→测试→反思→优化→验证→输出
- Reviewer 否决权 — 审查发现 🔴 阻塞项触发重写，最多 3 次迭代
- 复杂度自动分级 — A (Micro) / B (Feature) / C (System)，自动跳过不需要的阶段
- Risk Scorecard — 五元组量化检测，公用信号识别
- 状态持久化 — `.auto-coding/state.json`，仅保存任务恢复所需摘要，session 断了可恢复
- 审批策略 — `.auto-coding/rules.yaml`，默认收窄自动批准范围，敏感操作必须确认
- 进度汇报 — 默认前台逐阶段输出；可选开启通知或调度检查，默认不创建后台 cron

**Key features**:
- Full sub-agent architecture — main session only supervises; all work delegated to sub-agents
- Staged skill injection — each phase injects corresponding skill files, ≤2 skills per phase
- 8-step cycle — Design → Decompose → Code → Test → Reflect → Optimize → Verify → Output
- Reviewer veto power — 🔴 blockers trigger rewrite, up to 3 iterations
- Auto complexity grading — A (Micro) / B (Feature) / C (System), auto-skip irrelevant phases
- Risk Scorecard — 5-tuple quantified detection with public signal recognition
- State persistence — `.auto-coding/state.json`, stores resumable task summaries only
- Approval rules — `.auto-coding/rules.yaml`, narrow default auto-approval and require confirmation for sensitive actions
- Progress reporting — foreground per-phase output by default; optional notification/scheduler check only when explicitly enabled

---

## 设计哲学 / Design Philosophy

1. **思考优先** — 不假设，模糊需求列出假设或直接提问
2. **极简主义** — 最少代码解决问题，自检"200 行能否缩到 50 行"
3. **手术刀修改** — 只改必须改的，不顺手重构，遵循现有风格
4. **目标导向** — 先定义 Done 标准再编码，验证通过才算完成

1. **Think first** — Don't assume; list assumptions for ambiguous requirements or ask directly
2. **Minimalism** — Solve with minimal code; self-check "can 200 lines shrink to 50?"
3. **Scalpel edits** — Only change what's necessary; don't refactor opportunistically; follow existing style
4. **Goal-oriented** — Define Done criteria before coding; verification pass = completion

---

## 🔴 执行铁律

### 铁律 1: 自动推进，不中途停下
启动后连续完成所有阶段。只在 3 种情况打断: (1) 需求不明确 (2) 多方案需选择 (3) 安全审批。

### 铁律 2: 全子代理化，主会话只做监工
所有干活用子代理执行。主会话职责: 分阶段派活、检查文件质量、打回重写、交付结果。

### 铁律 3: 每步输出，不攒到最后
每阶段完成后立刻在当前会话输出结果（当前阶段、模型、做了什么、发现了什么），然后直接进入下一阶段。这是默认进度汇报机制，避免依赖后台 cron 或外部通知。

---

## 📋 8 步循环流程 + 技能注入

```
设计 → 分解 → 编码 → 测试 → 反思 → 优化 → 验证 → 输出
  ↑_______________________________________↓
              迭代 (最多 3 次)
```

| 步骤 | 阶段 | 注入技能 | 模型 | 职责 |
|------|------|---------|------|------|
| 1 | **设计** | `grill-with-docs` | `deepseek-v4-pro` | 需求对齐、技术方案 |
| 2 | **分解** | `decomposition` | `deepseek-v4-pro` | 任务拆解、依赖分析 |
| 3 | **编码** | `tdd` | `deepseek-v4-pro` | TDD 红-绿-重构 |
| 4 | **测试** | `testing` | `deepseek-v4-pro` | 边界覆盖、回归检测 |
| 5 | **反思** | `zoom-out` + `code-review` | `deepseek-v4-pro` | 审查、🔴🟡💭 分级 |
| 6 | **优化** | `optimize` | `deepseek-v4-pro` | 推理重构 |
| 7 | **验证** | `verification` | `deepseek-v4-pro` | 交付验证 |
| 8 | **输出** | — | — | 交付物 |

> **注入规则**: 每阶段 ≤2 技能文件，全局文件（`risk-scorecard` + `discipline-meta`）随首次注入附带。注入失败不阻塞流程。
>
> **Reviewer 否决权**: 审查发现 🔴 阻塞项（安全漏洞、不符合需求、过度设计）→ 触发重写，最多 3 次迭代。
> 详细见: `skills/code-review.skill.md`
>
> **调试子流程**: 测试失败或否决时触发 6 阶段调试（反馈循环→复现→假设→插桩→修复→清理）。
> 详细见: `skills/diagnose.skill.md`
>
> **模型适配**: 各阶段模型应根据自身模型配置进行重新适配，推荐采用多模型交叉检测与验证的方式，避免单一模型盲区。
>
> **Model adaptation**: Each phase's model should be re-adapted based on available model configuration. Multi-model cross-validation is recommended over single-model detection to avoid blind spots.

---

## ⚡ 复杂度自动分级

| 等级 | 特征 | 阶段数 | 典型耗时 |
|------|------|--------|---------|
| **A (Micro)** | 单函数、Bug 修复 | 编码→测试→验证 (3) | <2 分钟 |
| **B (Feature)** | 模块开发、单 API | 设计→编码→测试→验证 (4) | 2-5 分钟 |
| **C (System)** | 完整系统、多文件重构 | 设计→分解→编码→测试→反思→优化→验证 (7) | 5-15 分钟 |

> A 级至少注入 `grill-with-docs`（需求确认部分）。连续 2 次阻塞自动升级为 B 级。

---

## 🤖 模型分配 + 降级

| 阶段 | 首选 | Fallback 1 | Fallback 2 |
|------|------|-----------|-----------|
| 设计/分解 | `deepseek-v4-pro` | `MiMo v2.5 Pro` | — |
| 编码/测试 | `deepseek-v4-pro` | `MiMo v2.5 Pro` | — |
| 审查/优化 | `deepseek-v4-pro` | `MiMo v2.5 Pro` | — |
| 验证 | `deepseek-v4-pro` | `MiMo v2.5 Pro` | — |

**降级原则**: 优先同级别 → 降一级 → 记入日志。

---

## 📝 子代理铁律

所有子代理禁止输出完整内容到对话:

```
✅ {阶段}完成
📄 输出文件: {file1}, {file2}, ...
💡 一句话结论: {核心结论}
```

---

## 🧠 编码纪律（精简）

1. **思考优先**: 不假设，模糊需求列出假设或直接提问
2. **极简主义**: 最少代码解决问题，自检"200 行能否缩到 50 行"
3. **手术刀修改**: 只改必须改的，不顺手重构，遵循现有风格
4. **目标导向**: 先定义 Done 标准再编码，验证通过才算完成

---

## 📁 技能文件索引

| 技能文件 | 注入阶段 | 职责 |
|---------|---------|------|
| `skills/grill-with-docs.skill.md` | Step 1 设计 | 需求对齐、结构化追问、CONTEXT.md 维护 |
| `skills/decomposition.skill.md` | Step 2 分解 | 任务拆解纪律、依赖分析、粒度检查 |
| `skills/tdd.skill.md` | Step 3 编码 | TDD 红-绿-重构循环、垂直切片规则 |
| `skills/testing.skill.md` | Step 4 测试 | 测试策略、边界覆盖、回归检测 |
| `skills/zoom-out.skill.md` | Step 5 反思 | 全局视角、跨模块依赖分析 |
| `skills/code-review.skill.md` | Step 5 反思 | Reviewer 审查、🔴🟡💭 分级、Reviewer 否决权 |
| `skills/optimize.skill.md` | Step 6 优化 | 重构纪律、性能优化检查清单 |
| `skills/verification.skill.md` | Step 7 验证 | 交付验证清单、阶段聚合 |
| `skills/diagnose.skill.md` | 调试子流程 | 6 阶段系统化调试 |
| `skills/improve-architecture.skill.md` | Step 8.5 | 架构健康检查、深层耦合发现 |
| `skills/risk-scorecard.skill.md` | 全局（首次附带） | Risk Scorecard 五元组、公用信号检测规则 |
| `skills/discipline-meta.skill.md` | 全局（首次附带） | 元规则、量化上限、override 流程 |

---

## ⚠️ 安全透明声明

### 进度汇报策略

默认情况下，Auto-Coding **不创建后台 cron**，也**不主动发送飞书消息**。进度通过当前会话逐阶段输出：每完成一个阶段立即报告阶段名、产物、发现的问题和下一步。

如用户明确要求“后台跑完通知我 / 开启进度检查”，才启用可选通知机制：

| 模式 | 默认状态 | 数据流向 | 说明 |
|------|---------|---------|------|
| 前台逐阶段输出 | ✅ 默认开启 | 当前会话 | 每阶段完成后直接汇报，不产生后台任务 |
| 终态通知 | ❌ 默认关闭 | 用户指定通知通道 | 仅发送任务标题、任务 ID、阶段摘要和完成状态 |
| 调度检查 | ❌ 默认关闭 | 宿主调度器 | 仅在用户显式 opt-in 时创建；任务结束后自动删除，并提供手动清理指引 |

### 外部操作

| 操作 | 默认状态 | 数据流向 | 说明 |
|------|---------|---------|------|
| 模型推理 | 按宿主配置 | 任务描述 / 必要代码上下文 → 宿主模型服务 | 不读取或发送 API 密钥；具体模型网络路径由宿主环境决定 |
| 外部通知 | 默认关闭 | 阶段摘要 / 完成状态 → 用户指定通道 | 仅在用户显式开启时使用 |
| 环境配置 | 可选 | 本地配置 → 模型选择 | 仅读取非密钥模型选择项；不读取 `apiKey`、`baseUrl`、token 等敏感字段 |

### 文件系统

| 操作 | 范围 | 说明 |
|------|------|------|
| 读取 | 当前项目目录 | 读取需求相关代码、测试、配置和依赖文件 |
| 写入代码 | 当前项目目录 | 仅修改任务相关文件；敏感路径需审批 |
| 状态目录 | `.auto-coding/` | 保存 `state.json`、阶段摘要日志、审批状态和 scratchpad，用于恢复与审计 |

`.auto-coding/` 可能包含任务描述、文件路径、阶段摘要、测试结果和局部代码片段。建议将其加入 `.gitignore`，避免误提交；任务完成后可删除该目录清理本地状态。

### 模型环境变量

```
AUTO_CODING_MODEL_DESIGN=...     # 设计阶段模型覆盖
AUTO_CODING_MODEL_DECOMPOSE=...  # 分解阶段模型覆盖
AUTO_CODING_MODEL_CODE=...       # 编码阶段模型覆盖
AUTO_CODING_MODEL_TEST=...       # 测试阶段模型覆盖
AUTO_CODING_MODEL_REVIEW=...     # 审查阶段模型覆盖
AUTO_CODING_MODEL_OPTIMIZE=...   # 优化阶段模型覆盖
AUTO_CODING_MODEL_VERIFY=...     # 验证阶段模型覆盖
AUTO_CODING_FALLBACK_MODEL_1=... # 回退模型 1
AUTO_CODING_FALLBACK_MODEL_2=... # 回退模型 2
```

> 所有环境变量均为可选，只用于模型选择或降级策略，不应包含 API 密钥、Base URL、token 或其它敏感配置。

---

## 📦 使用示例

- **A 级**: `auto-coding：写一个 Python 函数计算两个列表的交集` → 编码→测试→验证
- **B 级**: `Auto coding：实现一个 REST API，支持用户注册和登录` → 设计→编码→测试→验证
- **C 级**: `启动自动编码：从零搭建一个博客系统，支持文章发布和评论` → 完整 7 阶段

---

## ⚙️ 项目配置

- **状态持久化**: `.auto-coding/state.json` — session 中断自动从上次阶段恢复
- **审批策略**: `.auto-coding/rules.yaml` — 默认仅自动批准文档类低风险修改；代码修改、命令执行和敏感路径默认要求确认
- **阶段日志**: `.auto-coding/logs/{order}-{phase}.log` — 每个阶段独立可追溯，建议不提交到版本库

---

*v3.7.17-compliance · 2026-06-09*
