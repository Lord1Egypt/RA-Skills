---
name: quality-verification
version: 2.0.0
description: 输出质量保障与验证。编辑后检查、提交前测试、session 指标测量。不适用于工具重试（用 tool-governance）或 agent 提前停止（用 execution-loop）。参见 tool-governance（错误追踪）。
license: MIT
triggers:
  - post edit check
  - lint after edit
  - test before commit
  - hook bracket
  - session metrics
  - quality gate
  - hook profile
author: OpenClaw Team
---

# Quality & Verification

输出质量保障：编辑后即时检查、提交前自动测试、per-turn 指标测量。

## When to Use

- 编辑后即时检查 → Post-edit diagnostics
- 提交前跑测试 → Test-before-commit gate
- 测量 per-turn 指标 → Hook pair bracket
- 按环境切换 hook 强度 → Hook runtime profiles

## When NOT to Use

- Agent 提前停止 → 用 `execution-loop`
- 工具安全 → 用 `tool-governance`

---

## Patterns

### 6.1 Post-Edit Diagnostics `[script]`

PostToolUse hook 在每次 Write/Edit 后立即跑 linter 或 type checker，通过 `additionalContext` 把错误注入当前 turn。这是 shift-left 策略——在错误扩散前秒级捕获，避免 agent 在类型错误的基础上继续编辑更多文件，导致级联放大。诊断工具按扩展名映射：`.ts` → tsc, `.py` → ruff/pyright, `.rs` → cargo check；扩展名不在映射表中的文件直接跳过，不空跑。→ [详见](references/post-edit-diagnostics.md)

### 6.2 Hook Runtime Profiles `[config]`

通过 `HARNESS_PROFILE` 环境变量控制 hook 行为强度，无需改 settings.json。三档：`minimal`（仅原子写入，快速实验用）、`standard`（日常开发）、`strict`（全部 pattern，生产变更和安全修复用）。还支持 `HARNESS_DISABLED_HOOKS` 按名字禁用单个 hook，粒度更细。→ [详见](references/hook-profiles.md)

### 6.3 Session Turn Metrics `[script]`

UserPromptSubmit + Stop 两个 hook 构成测量"括号"，在每轮交互前后采集时间戳和 context token 数。轮次结束时计算耗时和 token 增量，写入 `bracket.json` 供外部监控读取。只测量和记录，不阻止任何操作——与 ralph 的 Stop hook 叠加时，bracket 在前记录数据，ralph 在后决定是否 block。→ [详见](references/hook-bracket.md)

### 6.4 Test-Before-Commit Gate `[script]`

PreToolUse hook 拦截 `git commit` 命令，在 commit 执行前自动跑项目测试套件（按 package.json / Makefile / pyproject.toml / Cargo.toml 优先级检测测试命令）。测试失败时 deny commit 并把失败输出注入 context，agent 先修 bug 再提交。测试通过才放行，防止 broken commit 进入历史。→ [详见](references/test-before-commit.md)

### 6.5 Atomic State Writes `[design]`

所有状态文件（ralph.json、cancel.json、tool-errors.json 等）先写到 PID+时间戳命名的临时文件，再 `mv` 原子替换。POSIX 上 rename 是原子操作，读者要么看到旧版本要么看到新版本，不会读到半写的 JSON。多进程并发写入时每个进程写各自的临时文件，互不干扰。→ [详见](references/atomic-writes.md)

### 6.6 Session State Hygiene `[design]`

定期清理 4 类残留状态：超过 24h 仍 active 的 stale ralph.json、超过 30min 的 orphaned lock、只含 `.recovery-checked` 的空 session 目录、目录已删除但 git worktree list 中仍存在的 stale worktree 引用。支持 dry-run 预览，推荐每 4 小时或新 session 启动前运行。不清理的后果是 crash recovery 误识别 stale 状态为可恢复。→ [详见](references/session-hygiene.md)

## Scripts

| 脚本 | Hook 类型 | 功能 |
|------|----------|------|
| `post-edit-check.sh` | PostToolUse (Write\|Edit\|MultiEdit) | 编辑后 linter |
| `bracket-hook.sh` | Stop | 记录 per-turn 指标 |
| `test-before-commit.sh` | PreToolUse (Bash) | commit 前跑测试 |

## Workflow

文件被编辑？→ PostToolUse hook 触发 `post-edit-check.sh`，按扩展名选择 linter（`.ts` → tsc, `.py` → ruff, `.sh` → shellcheck），将诊断错误通过 `additionalContext` 注入当前 turn，agent 当场修复。编辑后立即跑诊断——拖到 commit 时再查，类型错误已经在错误基础上级联了好几个文件。扩展名不在映射表中的文件（如 `.md`）直接跳过。

要 git commit？→ PreToolUse hook 触发 `test-before-commit.sh`，拦截 Bash 中的 `git commit` 命令，跑完整测试套件。测试失败则 deny commit 并展示失败用例，agent 修完再提交。测试通过才放行。

<example>
场景: Post-edit diagnostics 即时捕获类型错误
触发: Agent 编辑 handlers.ts（PostToolUse hook 匹配 .ts 扩展名）
执行: post-edit-check.sh 跑 `tsc --noEmit`
输出: TS2345 错误通过 additionalContext 注入当前 turn
结果: Agent 同 turn 修复类型错误，错误没有传播到后续文件
</example>

<example>
场景: Test-before-commit 拦截 broken commit
触发: Agent 执行 `git commit -m "add user endpoint"`（PreToolUse hook 匹配 Bash 中的 git commit）
执行: test-before-commit.sh 检测到 package.json，跑 `npm test`
结果: 2 个测试失败，hook 输出 deny + 失败用例，Agent 先修 bug 再提交
</example>

<anti-example>
错误: 对 README.md 编辑跑 post-edit diagnostics
原因: .md 不在扩展名映射表中，没有 linter 可跑
处理: post-edit-check.sh 按扩展名过滤，无映射的文件 exit 0（不空跑）
</anti-example>

## Failure Modes

| 场景 | 处理 |
|------|------|
| Linter 自身 crash 或超时 | post-edit-check.sh 设 `timeout 30s` 执行 linter。超时或非零退出 → exit 0（不阻塞 agent），记录到 stderr |
| 找不到测试命令（4 种检测全部 miss） | test-before-commit.sh 无法检测到 package.json/Makefile/pyproject.toml/Cargo.toml → 跳过测试，allow commit，注入 warning "未检测到测试框架" |
| 测试运行时间过长 | 设 `timeout 300s`（5 分钟），超时 → deny commit + 注入 "测试超时，请检查是否有死循环或外部依赖" |
| bracket-hook.sh 无法读取 transcript | transcript 路径不可用或文件不存在 → 跳过指标记录，不影响 agent 执行 |
| 多个 PostToolUse hook 冲突 | Claude Code 按 settings.json 中的顺序依次执行，additionalContext 会 concatenate。post-edit-check 应排在 tool-governance 的 error-tracker 之前 |

## Output

| 产出物 | 来源 | 说明 |
|--------|------|------|
| 诊断结果 | `additionalContext` | linter/type checker 错误注入 agent 上下文，agent 当场可见 |
| session 指标 | `bracket.json` | per-turn 时间、turn 计数、hook 执行耗时 |
| 测试结果 | commit 前 | 测试套件输出，失败时 block commit 并展示失败用例 |

## Related

- `tool-governance` — 错误追踪器记录诊断失败（tool-error-tracker 追踪连续 linter 失败）
- `execution-loop` — doubt gate 检测未验证声明（agent 说"应该没问题"但没跑检查时拦截）
- `context-memory` — 诊断结果写入 handoff document，跨 session 传递未修复的已知问题


## Usage

在 `.claude/settings.json` 中配置 hook：

```jsonc
{
  "hooks": {
    // Post-edit 诊断：编辑后立即跑 linter
    "PostToolUse": [
      {
        "matcher": { "tool_name": "Write|Edit|MultiEdit" },
        "hooks": [
          {
            "type": "command",
            "command": "bash post-edit-check.sh \"$TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ],
    // Commit 前测试：拦截 git commit，测试不通过则 deny
    "PreToolUse": [
      {
        "matcher": { "tool_name": "Bash", "input_contains": "git commit" },
        "hooks": [
          {
            "type": "command",
            "command": "bash test-before-commit.sh"
          }
        ]
      }
    ]
  }
}
```

`post-edit-check.sh` 按扩展名选 linter：`.ts` → `tsc --noEmit`，`.py` → `ruff check + pyright`，`.rs` → `cargo check`，其他 → exit 0。

`test-before-commit.sh` 按项目类型检测：`package.json` → `npm test`，`Makefile` → `make test`，`pyproject.toml` → `pytest`，`Cargo.toml` → `cargo test`。

Hook 输出格式（post-edit-check.sh stdout）：
```json
{"decision": "allow", "hookSpecificOutput": {"additionalContext": "[POST-EDIT] tsc error TS2345: Argument of type 'string' is not assignable to parameter of type 'number' at handlers.ts:42"}}
```

按 profile 控制强度：
```bash
HARNESS_PROFILE=strict claude -p "deploy to production"   # 全部 hook
HARNESS_PROFILE=minimal claude -p "fix typo in README"     # 仅原子写入
HARNESS_DISABLED_HOOKS=post-edit-check claude -p "quick experiment"  # 禁用指定 hook
```
