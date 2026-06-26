---
name: devloop-workflow
description: >-
  Complete multi-agent collaboration workflow for product-driven development loops.
  Covers the full lifecycle from product discovery through architecture design,
  parallel coding, testing, to marketing. Includes 6 specialized agents
  (Product, Core Dev, Dev, Test, Marketing, Research) with defined roles,
  communication protocols, and shared file conventions.
  This skill should be used when setting up or understanding the DevLoop agent
  collaboration system, configuring agent workflows, troubleshooting inter-agent
  communication, resolving agent responsibility questions, or customizing agent
  behavior through SOUL.override.md and MEMORY.md.
version: 2.0.0
---

# DevLoop Workflow — 多 Agent 协作系统

产品驱动开发闭环 — 开箱即用的多 Agent 协作系统，覆盖从产品热点探索到开发测试上线的完整生命周期。

## Agent 清单

| Agent | ID | Emoji | 职责 |
|-------|-----|-------|------|
| Product | `devloop-product` | 🎯 | 每日 AI 热点探索、产品方向讨论、PRD 生成 |
| Core Dev | `devloop-core-dev` | 🧠 | 架构设计（7 维度）、设计文档、Dev 调度 |
| Dev | `devloop-dev` | ⚡ | 精准编码、多实例并行、按设计文档实现 |
| Test | `devloop-test` | 🧪 | 测试先行、Bug 趋势追踪、代码审查 |
| Marketing | `devloop-marketing` | 📣 | 商业化调研、宣传策略、文案制作 |
| Research | `devloop-research` | 🔬 | 深度调研、竞品分析、技术评估 |

## 核心工作流

```
阶段一：产品发现
  [Cron 触发] → 🎯 Product（热点探索 + 历史对比）

阶段二：方向讨论与 PRD
  用户 ↔ 🎯 Product 多轮讨论 → 确认方向 → 生成 PRD
       → 通知 🧠 Core Dev + 📣 Marketing

阶段三：设计与调度
  🧠 Core Dev（7维度讨论→设计文档→复杂度评估→调度）
       → 分配任务给 ⚡ Dev (×N)
       → 通知 🧪 Test 准备测试规格

阶段四：测试先行
  🧪 Test（读取设计文档 → 生成测试规格 → 通知 Dev 参考）

阶段五：编码实现
  ⚡ Dev ×N（严格按设计文档编码 → Conventional Commits → 报告完成）

阶段六：测试与合并
  🧪 Test（代码审查 + 测试执行 + Bug 记录）
  🧠 Core Dev 确认质量 → 合并到 main
       → 📣 Marketing（上线宣传）
```

完整的阶段细节、消息路由表和并行冲突预防规则，参见 `references/collaboration-protocol.md`。

## 通用工作规范

### Session 启动

1. 读取 `SOUL.override.md`（如存在，替代 `SOUL.md`），否则读取 `SOUL.md`
2. 读取 `USER.md`
3. 读取 `memory/YYYY-MM-DD.md`（今天 + 昨天）
4. **仅主 session**：读取 `MEMORY.md`

首次启动：若 `BOOTSTRAP.md` 存在，按其指引初始化后删除。

### 记忆管理

| 类型 | 路径 | 说明 |
|------|------|------|
| 每日笔记 | `memory/YYYY-MM-DD.md` | 当日工作日志（平面文件，不建子目录） |
| 主题笔记 | `memory/YYYY-MM-DD-<suffix>.md` | 按主题的专项日志 |
| 长期记忆 | `MEMORY.md` | 跨 session 持久知识（仅主 session 加载，含私人上下文） |

想记住的东西必须写文件。"心里记住"在 session 结束后消失。

### Agent 协作

通过 `sessions_send` 通信。共享文件通过各自 workspace 的 `shared/` 目录（只读消费，不修改，不用 `../` 路径）。

### 自定义

优先级：`SOUL.override.md` > `SOUL.md` > 各 Agent `.md`

### 安全

- 不泄露私人数据
- 破坏性命令先确认
- `trash` > `rm`

## 模板文件

所有模板位于本 skill 的 `assets/templates/` 目录。Agent 首次创建文件时，读取对应模板并按实际内容填充。

| 模板文件 | 用途 | 使用者 |
|----------|------|--------|
| `project-structure.template.md` | 项目知识库结构 | Product, Marketing |
| `design-doc.template.md` | 功能设计文档 | Core Dev |
| `design-index.template.md` | 设计文档索引 | Core Dev |
| `test-spec.template.md` | 测试规格文档 | Test |
| `daily-report.template.md` | 每日测试报告 | Test |
| `bug-tracker.template.md` | Bug 追踪数据库 | Test |
| `review-notes.template.md` | PR 审查笔记 | Test |
| `bug-trend.template.md` | Bug 趋势汇总（MEMORY.md 用） | Test |
| `memory-tracking.template.md` | 调研方向追踪表（MEMORY.md 用） | Product, Marketing |

## 参考资料

需要深入了解时，加载以下 references 文件：

| 文件 | 何时加载 | 内容 |
|------|----------|------|
| `references/collaboration-protocol.md` | 需要了解 Agent 间通信细节、消息格式、文件共享规则、完整工作流阶段细节时 | 完整协作协议、消息路由表、共享目录约定、并行冲突预防 |
| `references/agent-design-background.md` | 需要理解设计决策背景、处理边缘情况时 | 各 Agent 的设计理念、权限说明、边缘情况处理方案 |

快速查找关键信息：
- Agent 间消息格式：搜索 `sessions_send` in `references/collaboration-protocol.md`
- 文件共享规则：搜索 `shared/` in `references/collaboration-protocol.md`
- 并行冲突处理：搜索 `交叉` in `references/collaboration-protocol.md`
- 各 Agent 权限设计：搜索 `权限设计` in `references/agent-design-background.md`
- 边缘情况处理：搜索 `边缘情况` in `references/agent-design-background.md`

## 前置要求

- OpenClaw 2026.3.x+
- Linux / macOS（Windows 需 WSL）
