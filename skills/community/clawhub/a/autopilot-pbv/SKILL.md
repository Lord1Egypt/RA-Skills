---
name: autopilot
description: 自动循环编排引擎 — Plan(OMC opus) → Build(OMX) → Verify(Orchestrator) 循环执行复杂任务，最多5轮自动收敛。当用户提到"自动执行"、"循环执行"、"帮我自动完成"、需要多步验证的复杂重构、自动修复循环、多模块联动修改时触发。即使用户没有明确说"autopilot"，只要任务复杂度需要计划→执行→验证→修复的循环，就应该建议使用本技能。简单单文件修改直接派发 OMC 或 OMX 即可。
version: 2.2.0
metadata:
  openclaw:
    os: ["darwin", "linux"]
    requires:
      bins: ["claude", "omx", "python3"]
author: user
source: user-created
created_at: '2026-04-29'
updated_at: '2026-04-30'
---

# Autopilot — Plan → Build → Verify 自动循环

## 前置条件

- **`claude -p` 需要 `ANTHROPIC_API_KEY`**：Claude Code 的 `-p/--print` 管道模式依赖 API Key 认证，不支持 OAuth 交互登录。设置：`export ANTHROPIC_API_KEY="sk-ant-..."`
- `claude` CLI 已安装
- `omx` CLI 已安装
- Python 3.9+

Autopilot 让 编排器自动驱动复杂编码任务走向收敛：OMC(opus) 出结构化计划，OMX 按计划写代码（默认 GPT 最新模型），编排器跑测试验证。验证不通过就带着错误报告回到 OMC 重新规划，最多 5 轮。

为什么需要循环？因为单次派发 OMC 或 OMX 适合简单任务，但复杂任务（系统重构、多模块联动、需要测试回归验证）往往一次做不对。Autopilot 通过 Plan→Build→Verify 循环逐步收敛，每轮都知道上一轮哪里错了。

## 快捷指令

| 指令 | 用途 |
|------|------|
| `启动 autopilot <描述>` 或 `启动 autopilot <描述>` | 启动自动循环 |
| `启动 autopilot <描述> -d <目录>` | 指定工作目录 |
| `查看状态 <task_id>` | 查看任务状态和轮次 |
| `恢复任务 <task_id>` | 恢复中断的任务 |

> 匹配规则：消息以 "autopilot" 或 "自动执行" 开头即触发。`-d` 后的路径运行时展开为绝对路径，`task.json` 和命令中禁止保存 `~` 简写。

## 核心角色分工

| 角色 | 谁来做 | 做什么 |
|------|--------|--------|
| **Orchestrator** | 编排器 | 理解需求、补充上下文、驱动循环、检查计划、验证结果、决定继续或退出 |
| **Planner** | OMC (claude opus) | 只读分析项目，输出结构化 `plan-{round}.md`，不修改任何文件 |
| **Builder** | OMX (omx exec) | 根据 plan 写代码、修改文件、补测试 |
| **Verifier** | 编排器 | 跑测试、检查 git diff、逐条比对验收标准 |

为什么这样分工？OMC 的 opus 模型擅长深度分析和结构化思考但不应该动文件；OMX 擅长执行但需要精确指令；验证由编排器自己做是因为 编排器能直接跑测试和读文件，最可靠。

**关键约束**：三个角色之间没有共享内存——所有上下文必须通过任务目录的文件传递。这是设计而非限制：文件传递让每个 agent 拿到的上下文是明确可控的，不会因为隐式上下文导致不一致。

## 循环控制

最多 5 轮（`pbv_max_rounds = 5`）。每轮生成独立的 `plan-{round}.md`、`result-{round}.txt`、`verify_report-{round}.md`。

**退出条件**（任一满足即退出）：
- ✅ `verify_passed`：验收标准全通过，成功退出
- 🛑 `max_rounds(5)`：第 5 轮仍失败，汇报最佳结果和剩余问题
- 🛑 `consecutive_same_error(2轮)`：连续两轮 P0 问题相同——说明当前方案解决不了，再试也是烧钱
- 🛑 `no_progress`：连续两轮验证报告高度相似（问题汇总+修复方向相似度 >80%）
- ⏹ `user_cancel`：用户主动取消，保留任务目录供 恢复操作

plan 质量不达标时允许本轮内重试最多 2 次（不增加 `pbv_round`），因为 plan 是整个循环的基础——plan 错了后面全白费。

## 编排流程

### Phase 0: 初始化

1. 解析指令：提取任务描述、`-d` 工作目录（未提供时用当前会话工作目录）
2. **预检**（复用 omc-omx-orchestrator 的 Step 0 逻辑）：
   - 工作目录存在且为目录
   - `which claude` 和 `which omx` 都有输出
   - 非 git 目录时设置 `sandbox_args="--skip-git-repo-check"`
3. 创建任务目录：`~/.openclaw/workspace/tasks/{timestamp}-{slug}/`
4. 写 `task.json`（扩展字段见下方）
5. 写 `spec_plan.md`：用户原始需求 + 编排器补充的上下文（项目路径、技术栈、当前分支、约束、初始验收标准）

### Phase 1: Plan（OMC）

1. 更新 `pbv_round += 1`，`pbv_status = planning`
2. 构建 OMC 命令，spec_plan.md 作为输入，输出重定向到 `plan-{round:03d}.md`：

```bash
cat {task_dir}/spec_plan.md | \
claude -p --output-format text --verbose --model claude-opus-4-6 - \
  > {task_dir}/plan-{round:03d}.md \
  2> {task_dir}/plan-{round:03d}.log ; \
echo $? > {task_dir}/plan-{round:03d}.exit_code
```

> ⚠️ **绝不加 `--max-turns`** — text 模式下 `max-turns` 会过早终止输出。text 模式无 JSONL 膨胀问题，不需要限制 turns。

3. OMC 崩溃时重试一次；仍失败则终止任务
4. **编排器检查 plan 质量**：
   - 有 `## 执行步骤` 和至少一个 `### Step`
   - 有明确可验证的验收标准
   - 有 `## 文件清单`
   - 不通过则补充要求重新生成（本轮内最多 2 次，不算新轮次）

### Phase 2: Build（OMX）

1. 从 plan 构建 `spec_build.md`——必须包含完整上下文：用户需求、项目路径、当前轮计划、上一轮失败摘要（如有）、约束、验收标准、允许修改的文件清单
2. 更新 `pbv_status = building`
3. 构建 OMX 命令：

```bash
cat {task_dir}/spec_build.md | \
omx exec --dangerously-bypass-approvals-and-sandbox \
  -o {task_dir}/result-{round:03d}.txt \
  -C {cwd} \
  {sandbox_args} - \
  2> {task_dir}/build-{round:03d}.log ; \
echo $? > {task_dir}/build-{round:03d}.exit_code
```

4. OMX 崩溃时重试一次；仍失败则终止任务
5. 更新 `pbv_status = build_done`

### Phase 3: Verify（编排器）

1. 更新 `pbv_status = verifying`
2. 从 `plan-{round}.md` 提取验收标准和文件清单
3. 运行验证（详见 `references/verify-guide.md`）：
   - **测试**：优先 `项目测试脚本（如 scripts/run_tests.sh、pytest 等）`，否则 `pytest`/`npm test` 等；无测试时记录 ⚠️
   - **文件变更**：`git diff --stat` 检查实际修改是否和 plan 一致
   - **验收标准**：逐条核对，给出 ✅/❌/⚠️ + 证据
4. 写 `verify_report-{round:03d}.md`（格式见 `references/verify-guide.md`）
5. 通过 → Phase 4；失败 → 提取错误摘要（≤500字），检查退出条件，未触发则回到 Phase 1

### Phase 4: 交付

1. 汇总所有轮次的 plan/result/verify_report
2. 更新 `task.json`：`status=completed`、`completed_at=<ISO时间>`
3. 通知用户：成功时给验证命令；失败时给退出原因和下一步建议

## task.json 扩展字段

在 omc-omx-orchestrator 基础 schema 上增加：

```json
{
  "mode": "autopilot",
  "engine": "autopilot",
  "pbv_round": 0,
  "pbv_status": "planning",
  "pbv_max_rounds": 5,
  "pbv_history": [
    {"round": 1, "plan": "plan-001.md", "result": "verify_failed", "error_summary": "..."}
  ]
}
```

`pbv_status` 流转：`planning` → `plan_done` → `building` → `build_done` → `verifying` → `verify_passed` / `verify_failed`

## 成本预估

| 场景 | 轮次 | 耗时 | 成本 |
|------|------|------|------|
| 简单（1轮过） | 1 | 8-22 min | ~$7.65 |
| 中等 | 2-3 轮 | 16-66 min | ~$15-23 |
| 复杂（4-5轮） | 4-5 轮 | 32-110 min | ~$30-38 |

每轮：OMC ~$1.50 + OMX ~$6.00 + Verify ~$0.15。5轮上限 + 相同错误退出 + 无进展退出 控制成本。

## 故障处理

- **OMC/OMX 崩溃或超时**：重试一次，仍失败则编排器可选择直接接管执行（而非终止任务）
- **编排器中断**：`恢复任务 <task_id>` 从 `pbv_status` 和 `pbv_round` 继续
- **plan 质量不达标**：本轮内最多重试 2 次，不算新轮次
- **无测试**：不能仅因无测试而判定通过，必须逐条验收

### 外部 Agent 全部失败时的编排器接管

当 OMC（Plan）和 OMX（Build）均超时或失败时，编排器作为 Orchestrator 可以直接接管：

1. **Plan 接管**：编排器直接分析需求，写 `plan-{round}.md`
2. **Build 接管**：编排器直接执行文件修改、创建脚本等
3. **Verify**：始终由编排器执行

适用条件：
- 任务需求明确，编排器能理解技术栈和目标
- 不需要深度分析复杂项目结构
- 文件数量可控（<10 个新建/修改）

### Plan 阶段 OMC 故障恢复

**text 模式（默认）故障**：
1. 输出格式不规范 → 补充 `spec_plan.md` 中的格式要求重试
2. 截断 → 检查是否 spec_plan.md 过大，精简后重试

**stream-json 模式故障**：
1. 上下文爆炸（tool 调用过多）→ 降低 `--max-turns` 或改用 text 模式
2. MCP 权限请求循环 → 改用 text 模式
3. 输出全是 JSONL 错误事件 → 改用 text 模式

⚠️ **text 模式绝不加 `--max-turns`** — 会立即终止输出。stream-json 模式必须加 `--max-turns 30-50`。

### Build 阶段 OMX 模型不可用

OMX (Codex) 使用 ChatGPT 账号时，不支持外部模型名（`o3`、`claude-sonnet-4` 等全部报 400）。

**恢复**：改用 OMC 替代 OMX 执行 Build 阶段：
```bash
cat "$TASK_DIR/spec_build.md" | \
claude -p --output-format text --verbose \
  --model claude-sonnet-4-20250514 \
  --dangerously-skip-permissions - \
  > "$TASK_DIR/result-001.txt" 2> "$TASK_DIR/build-001.log"
```

技巧：spec 里已经包含完整的修复方案和精确的代码 diff，OMC 只需照做即可，不需要 OMX 级别的自主决策能力。

## 与现有技能的关系

- **依赖 omc-omx-orchestrator**：本技能的 Plan 和 Build 阶段分别调用 OMC（`claude -p`）和 OMX（`omx exec`），复用其命令模板、目录结构、预检逻辑
- 共享 `~/.openclaw/workspace/tasks/` 和 `task-recovery.py`
- 不修改 omc-omx-orchestrator；`/omc` `/omx` 继续服务单次派发
- 循环控制逻辑完全在本 SKILL.md 中，不创建额外 Python 脚本

## 上下文管理策略

Plan 阶段的 OMC（opus）容易爆上下文，因为 opus 倾向深度阅读所有相关文件。Build 阶段的 OMX 相对稳定（执行型任务）。

**Plan 阶段（OMC）管道模式**：

默认使用 **text 模式**（`--output-format text`，不加 `--max-turns`）。优势：
- 无 JSONL 膨胀，上下文利用率高
- 适合大多数计划生成场景（Round 1 的深度分析 + Round 2+ 的修复规划）
- 不需要 `--input-format stream-json` 的 JSON 封装

**何时用 stream-json**：
- 轻中度任务（不需要深度探索项目结构）
- OMC 只需读少量文件 + 产出 plan
- 必须加 `--max-turns 30-50` 防止 JSONL 膨胀撑爆上下文
- ⚠️ stream-json 下 tool 调用次数受限（30-50），**无法完成复杂分析任务**

**核心区别**：

| | text 模式（默认） | stream-json 模式 |
|---|---|---|
| tool 调用 | 不限轮次，OMC 自由探索 | 限制 30-50 轮（JSONL 膨胀） |
| 上下文 | 纯文本，无膨胀 | JSONL 元数据膨胀快 |
| 适合场景 | 复杂深度分析（默认） | 轻中度任务、简单修复计划 |
| max-turns | 不设 | 必须 30-50 |

stream-json 命令（轻中任务备选）：
```bash
cd {cwd} && \
python3 -c "import json, pathlib; \
  p = pathlib.Path('{task_dir}/spec_plan.md'); \
  print(json.dumps({'type':'user','message':{'role':'user','content': \
    p.read_text() + '\n\n要求：只读分析，输出符合 autopilot plan 格式的结构化计划，不要修改文件。'}}))" | \
claude -p --input-format stream-json --output-format stream-json \
  --verbose --max-turns 40 --model claude-opus-4-6 --tools default - \
  > {task_dir}/plan-{round:03d}.md \
  2> {task_dir}/plan-{round:03d}.log ; \
echo $? > {task_dir}/plan-{round:03d}.exit_code
```

## plan.md 格式（OMC 必须遵循）

```markdown
# Plan: {task description}
> Round: {round_number} | Task: {task_id}

## 任务概述
{一段话说清楚要达成什么}

## 执行步骤

### Step 1: {标题}
- **目标**: {本步骤要达成的目标}
- **操作**: {具体要做什么}
- **预期输出**: {完成后应该看到什么}
- **验收标准**:
  - [ ] {可验证标准1}

## 文件清单
| 文件路径 | 操作 | 说明 |
|---------|------|------|

## 风险点
1. {风险}: {缓解措施}

## 完成标准
- [ ] 所有Step执行完成
- [ ] 所有验收标准通过
- [ ] 测试套件通过
```

## verify_report.md 格式（编排器必须遵循）

```markdown
# Verify Report - Round {round_number}
> Task: {task_id} | Status: PASSED/FAILED

## 总结
{一句话描述验证结果}

## 验证详情

### 测试运行
- **命令**: {执行的测试命令}
- **退出码**: {code}
- **结果**: PASSED/FAILED
- **关键错误**: {前5个最关键的错误，去重去噪}

### 文件变更检查
- **预期修改**: {plan中的文件清单}
- **实际修改**: {git diff结果}
- **差异**: {不在plan中但被修改的文件}

### 验收标准核对
| 标准 | 状态 | 备注 |
|------|------|------|
| {标准1} | ✅/❌/⚠️ | {说明} |

## 问题汇总
1. **P0**: {关键问题}
2. **P1**: {重要问题}

## 建议修复方向
1. {针对P0的修复建议}
```

错误摘要规则：只保留 P0/P1，每个一句话+文件定位，总长 ≤500字，P0 优先截断。连续两轮 P0 相同 → `consecutive_same_error` 退出。

## 参考文件

详细说明和检查清单在 `references/` 目录：

- `references/plan-format.md` — plan 格式设计要点 + Plan 检查清单
- `references/verify-guide.md` — 验证操作完整步骤 + 错误摘要生成规则详解 + 500字限制原因
