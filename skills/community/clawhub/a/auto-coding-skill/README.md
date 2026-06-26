# Auto-Coding v3.7.17

**版本**: v3.7.17  
**更新日期**: 2026-06-09

---

## 概述

Auto-Coding 是一个智能自主编码系统，通过多角色 Soul + 多模型切换，完成从需求到代码的完整开发流程：

```text
设计 → 分解 → 编码 → 测试 → 反思 → 优化 → 验证 → 输出
```

**本质**：单进程串行 + 多角色 Prompt + 多模型切换。不是真正的多 Agent 并行，而是每一步换不同的人格和模型来审视代码。

## 触发方式

为避免误触发高权限编码流程，ClawHub 版仅建议使用以下明确触发词：

- `auto-coding`
- `Auto coding`
- `启动自动编码`

不要用泛化词如“写代码”“开发”“coding”作为自动触发词。

---

## 合规版核心调整

### 1. 进度汇报：默认前台汇报，不默认创建 cron

Auto-Coding 任务步骤多，确实需要持续汇报。合规版采用三层策略：

| 层级 | 默认状态 | 用途 | 合规边界 |
| --- | --- | --- | --- |
| 当前会话逐阶段输出 | ✅ 默认开启 | 每阶段完成后立即报告阶段、产物、风险和下一步 | 不创建后台任务，不外发消息 |
| 状态文件恢复 | ✅ 默认开启 | session 中断后从 `.auto-coding/state.json` 恢复 | 仅写本地项目目录 |
| 后台调度 / 外部通知 | ❌ 默认关闭 | 用户离开会话后需要终态通知或进度检查 | 必须用户显式 opt-in，任务结束后清理 |

因此，不做默认 cron 并不等于没有进度：**前台执行时每一步都会汇报**。只有当用户明确说“后台跑完通知我 / 开启进度检查”时，才建议由宿主环境创建可清理的调度任务。

### 2. 飞书 / 外部通知：默认关闭，显式开启

飞书通知不是默认行为。启用后只发送最小必要摘要：任务标题、任务 ID、当前阶段、完成状态、少量阶段摘要。不会发送 API Key、token、完整代码或大段上下文。

### 3. 状态、日志、scratchpad

Auto-Coding 会在项目内写入 `.auto-coding/`，用于恢复、审批和审计。可能包含：

- `state.json`：任务 ID、阶段状态、完成状态、时间戳。
- `logs/`：阶段摘要、测试结果、风险评分。
- `pending_approval.json`：等待用户确认的操作。
- scratchpad / output：中间推理摘要或交付摘要。

合规建议：

- `.auto-coding/` 已加入 `.gitignore`。
- 不应提交 `.auto-coding/` 到远程仓库。
- 任务完成后可删除 `.auto-coding/` 清理本地状态。

### 4. 自动批准策略收窄

默认仅自动批准低风险文档变更：

```yaml
auto_approve:
  edit:
    - "docs/*"
    - "*.md"
  run: []
  create:
    - "docs/*"
    - "*.md"
```

以下操作默认需要确认：

- 修改代码文件：`*.py`、`*.js`、`*.ts`、`src/*`、`tests/*` 等。
- 修改配置、CI、环境文件。
- 删除任何文件。
- 运行任何命令，包括测试和构建命令。

### 5. 表达式求值与命令执行

- 风险阈值表达式使用 AST 白名单解释器，不使用动态代码执行。
- 技能默认不通过 CLI 创建 cron，也不默认执行外部命令。
- 需要运行测试、构建、发布、调度等命令时，必须经审批规则确认。

---

## 快速开始

```python
import asyncio
from workflow_enhanced import AutoCodingWorkflowEnhanced

async def main():
    workflow = AutoCodingWorkflowEnhanced(
        requirements="auto-coding：实现用户登录功能",
        project_dir="./my-project",
        resume=True,
    )
    await workflow.run()

asyncio.run(main())
```

第一次运行会生成配置模板：

- `.auto-coding/workflow.yaml.template`
- `.auto-coding/rules.yaml.template`

复制为实际配置后即可自定义阶段和审批策略。

---

## 文件清单

| 文件 | 说明 |
| --- | --- |
| `auto_coding_workflow.py` | 主工作流（八步循环） |
| `workflow_enhanced.py` | 增强版（状态 + 审批 + 前台进度汇报） |
| `workers/base_worker.py` | Worker 基类（含模型调用） |
| `workers/reviewer_worker.py` | ReviewerWorker（否决权） |
| `approval_rules.py` | 审批规则引擎，默认收窄 auto-approve |
| `scorecard_engine.py` | 风险评分与阈值判断 |
| `state_manager.py` | 状态持久化 |
| `SKILL.md` | Skill 入口文档 |

---

## 数据处理透明度

| 行为 | 默认状态 | 数据范围 | 用户控制 |
| --- | --- | --- | --- |
| 读取项目文件 | 开启 | 当前任务相关代码、测试、配置 | 通过任务范围和项目目录控制 |
| 写入代码文件 | 按需 | 当前项目目录内任务相关文件 | 敏感文件需确认 |
| 写入 `.auto-coding/` | 开启 | 状态、日志、审批、scratchpad | 可删除；应加入 `.gitignore` |
| 模型推理 | 按宿主环境 | 任务描述与必要代码上下文 | 由宿主模型配置决定 |
| 外部通知 | 默认关闭 | 任务 ID、阶段摘要、完成状态 | 仅显式开启 |
| 后台调度 | 默认关闭 | 任务 ID、状态检查摘要 | 仅显式开启，结束后清理 |

> 隐私提醒：如果任务涉及敏感业务逻辑，`.auto-coding/`、模型上下文和可选通知摘要都可能包含相关信息。请限制项目目录、关闭外部通知，并在任务完成后清理状态目录。

---

## 更新日志

| 版本 | 日期 | 关键变更 |
| --- | --- | --- |
| v3.7.17 | 2026-06-09 | ClawHub 合规修正：收窄触发词、默认关闭 cron/通知、收窄 auto-approve、披露 `.auto-coding/`、移除动态表达式执行 |
| v3.7.x | 2026-05 | 全子代理架构、分阶段技能注入、Reviewer 否决权、Risk Scorecard |

---

*Last updated: 2026-06-09 | Auto-Coding v3.7.17 compliance release*
