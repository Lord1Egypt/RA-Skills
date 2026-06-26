# Execution Harness

Make Claude Code agents finish their work.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-hooks%20compatible-blueviolet)]()
[![Patterns: 40](https://img.shields.io/badge/core%20patterns-40-orange)]()
[![Tests: 90](https://img.shields.io/badge/tests-90%20passing-brightgreen)]()

Agent 改了 7 个文件中的 2 个就停了。`cargo build` 在没有 cargo 的容器里重试了 12 次。压缩后忘了所有设计决策。5 个 agent 同时编辑同一个文件。限速后 tmux session 挂死 30 分钟没人管。

17 个 bash hook 脚本 + 23 个设计模式 = 40 patterns，覆盖 agent 可靠性的 6 个维度。不是框架，不做模型调用——只管住执行层。

## Quick Start

```bash
git clone https://github.com/lanyasheng/execution-harness.git
cd execution-harness
```

最小配置——把 3 个 hook 加到 `~/.claude/settings.json`：

```jsonc
{
  "hooks": {
    "Stop": [{
      "hooks": [
        {"type": "command", "command": "bash execution-loop/scripts/ralph-stop-hook.sh"},
        {"type": "command", "command": "bash execution-loop/scripts/doubt-gate.sh"}
      ]
    }],
    "PreToolUse": [{
      "hooks": [
        {"type": "command", "command": "bash tool-governance/scripts/tool-error-advisor.sh"},
        {"type": "command", "command": "bash tool-governance/scripts/tool-input-guard.sh"}
      ]
    }],
    "PostToolUse": [{
      "matcher": {"tool_name": "Write|Edit|MultiEdit"},
      "hooks": [
        {"type": "command", "command": "bash quality-verification/scripts/post-edit-check.sh"}
      ]
    }]
  }
}
```

```bash
# 启动持续执行（最多 50 轮，crash 后自动恢复）
bash execution-loop/scripts/ralph-init.sh my-task 50
```

这 3 个 hook 解决最常见的 3 个问题：agent 提前停（Ralph）、危险命令（input guard）、编辑后没跑 linter（post-edit check）。其余按需加。

## 解决什么问题

| 你遇到的问题 | 用哪个 pattern |
|-------------|---------------|
| Agent 只做了一部分就停了 | **1.1 Ralph** — Stop hook 阻止提前退出，5 个安全阀保底 |
| "应该可以" 但没跑测试 | **1.2 Doubt Gate** — 检测投机语言，要求验证 |
| `cargo build` 重试 12 次 | **2.1 Tool Error Escalation** — 3 次提示、5 次 block |
| `rm -rf` 毁了未提交的代码 | **2.3 Checkpoint + Rollback** — 破坏性命令前 git stash |
| 压缩后忘了设计决策 | **3.1 Handoff Documents** — 决策写磁盘，压缩删不掉 |
| Context 快满了还在读大文件 | **3.4 Token Budget** — 注入预算感知，80%+ 禁止直读 |
| 限速后 tmux 挂死 | **5.1 Rate Limit Recovery** — cron 扫描 pane 自动恢复 |
| 5 个 agent 编辑同一文件 | **4.3 File Claim and Lock** — 10 分钟 TTL 排他锁 |
| 长 session 偏离原始任务 | **1.5 Drift Re-anchoring** — 每 N 轮重新注入任务描述 |
| 提交了编译不过的代码 | **6.4 Test-Before-Commit** — commit 前自动跑测试 |
| 后台 agent 限速时疯狂重试 | **5.7 Anti-Stampede** — 后台任务遇 529 立即放弃 |

## 6 轴架构

每个轴是独立的 Claude Code skill。只装你需要的，忽略其余。

```
execution-harness/
├── principles.md                    ← 10 条设计原则
├── execution-loop/                  ← 7 patterns — 让 agent 做完再停
│   ├── SKILL.md
│   ├── scripts/                     ralph, doubt-gate, drift-reanchor, task-completion
│   ├── tests/
│   └── references/
├── tool-governance/                 ← 6 patterns — 工具使用安全
│   ├── SKILL.md
│   ├── scripts/                     error-tracker, error-advisor, input-guard, checkpoint
│   └── references/
├── context-memory/                  ← 8 patterns — 知识跨压缩存活
│   ├── SKILL.md
│   ├── scripts/                     context-usage, compaction-extract
│   └── references/
├── multi-agent/                     ← 6 patterns — 多 agent 协同（全部 design）
│   ├── SKILL.md
│   └── references/
├── error-recovery/                  ← 7 patterns — 故障恢复
│   ├── SKILL.md
│   ├── scripts/                     rate-limit-recovery
│   └── references/
└── quality-verification/            ← 6 patterns — 输出质量保障
    ├── SKILL.md
    ├── scripts/                     post-edit-check, bracket-hook, test-before-commit
    └── references/
```

轴之间没有硬依赖，但有协作：tool-governance 的错误数据喂给 error-recovery 做降级决策；execution-loop 的阶段边界触发 context-memory 写 handoff；quality-verification 的诊断结果流入 tool-governance 的错误追踪。

## 40 Core Patterns

### Execution Loop (7) — [SKILL.md](execution-loop/SKILL.md)

| # | Pattern | Type | 做什么 |
|---|---------|------|--------|
| 1.1 | Ralph persistent loop | script | Stop hook 阻止提前退出，5 个安全阀保底（context ≥95% / 401/403 / cancel / 闲置 2h / 迭代上限） |
| 1.2 | Doubt gate | script | 检测 "可能""大概" 等投机语言，要求提供证据 |
| 1.3 | Adaptive complexity triage | design | 按任务复杂度自动选 harness 强度——改 typo 不需要全套 |
| 1.4 | Task completion verifier | script | 读 `.harness-tasks.json`，有未完成项就不让停 |
| 1.5 | Drift re-anchoring | script | 每 N 轮重新注入原始任务描述，防跑偏 |
| 1.6 | Headless execution control | config | `-p` 模式没有 Stop hook，用 `--max-turns` + budget 注入替代 |
| 1.7 | Iteration-aware messaging | design | 第 5 轮和第 45 轮的 block 消息不该一样 |

### Tool Governance (6) — [SKILL.md](tool-governance/SKILL.md)

| # | Pattern | Type | 做什么 |
|---|---------|------|--------|
| 2.1 | Tool error escalation | script | 连续 3 次提示、5 次 deny（用 input hash 区分重试和新尝试） |
| 2.2 | Denial circuit breaker | script | 追踪用户否决次数，3 次后建议替代方案 |
| 2.3 | Checkpoint + rollback | script | `rm -rf` 等破坏性命令前自动 `git stash` |
| 2.4 | Graduated permission rules | config | 按风险分层：读文件放行，写文件确认，`rm` 拦截 |
| 2.5 | Component-scoped hooks | config | 不同任务启用不同 hook 组合 |
| 2.6 | Tool input guard | script | 拦截 `rm -rf /`、`curl \| sh` 等已知危险模式 |

### Context & Memory (8) — [SKILL.md](context-memory/SKILL.md)

| # | Pattern | Type | 做什么 |
|---|---------|------|--------|
| 3.1 | Handoff documents | design | 阶段边界写 Decided/Rejected/Risks/Files/Remaining 五段到磁盘 |
| 3.2 | Compaction memory extraction | script | Stop hook 每 15 轮快照关键决策到 handoff |
| 3.3 | Three-gate memory consolidation | design | 跨 session 记忆合并（Time ≥24h → Session ≥5 → FileLock） |
| 3.4 | Token budget allocation | design | 按 context 使用率梯度注入行为指令（<40% 自由 → ≥95% 必须放行） |
| 3.5 | Context token count | script | 从 transcript 提取 input_tokens（无法获取窗口百分比） |
| 3.6 | Filesystem as working memory | design | `.working-state/current-plan.md` + `decisions.jsonl` |
| 3.7 | Compaction quality audit | design | 压缩后对照 decisions.jsonl 检查关键决策是否存活 |
| 3.8 | Auto-compact circuit breaker | design | 连续 3 次 compact 失败后停止尝试，等 Reactive Compact (413) |

### Multi-Agent Coordination (6) — [SKILL.md](multi-agent/SKILL.md)

全部 design pattern——多 agent 编排差异太大，硬编码脚本反而限制适用性。

| # | Pattern | 做什么 |
|---|---------|--------|
| 4.1 | Three delegation modes | Coordinator / Fork / Swarm 选型（不确定→Coordinator） |
| 4.2 | Shared task list protocol | `.coordination/tasks.json` + mkdir 原子锁 + 指数退避 |
| 4.3 | File claim and lock | `.claims/*.lock` 排他锁，10 分钟 TTL，PreToolUse hook 检查 |
| 4.4 | Agent workspace isolation | 每个 agent 独立 `git worktree`，根源消除文件冲突 |
| 4.5 | Synthesis gate | coordinator 必须综合 research 结果，不当邮局转发 |
| 4.6 | Review-execution separation | 实现和审查用隔离 session 的不同 agent，盲审消除确认偏误 |

### Error Recovery (7) — [SKILL.md](error-recovery/SKILL.md)

| # | Pattern | Type | 做什么 |
|---|---------|------|--------|
| 5.1 | Rate limit recovery | script | cron 扫描 tmux pane，二次验证后发 Enter 恢复 |
| 5.2 | Crash state recovery | design | 扫描残留 ralph.json（>2h stale）和过期 lock（>15min） |
| 5.3 | Stale session daemon | design | heartbeat 超时 + tmux 不存在 → 从 transcript 抢救知识 |
| 5.4 | MCP reconnection | design | 指数退避 1→2→4→8→16s，5 次失败后注入 fallback 建议 |
| 5.5 | Graceful tool degradation | design | 连续 2 次失败后查 fallback 映射表注入降级建议 |
| 5.6 | Model fallback advisory | design | 3 次失败后建议升级模型 `[ADVISORY ONLY]` — hook 切不了模型 |
| 5.7 | Anti-stampede retry asymmetry | design | 前台 529 可重试，后台 529 立即放弃不重试 |

### Quality & Verification (6) — [SKILL.md](quality-verification/SKILL.md)

| # | Pattern | Type | 做什么 |
|---|---------|------|--------|
| 6.1 | Post-edit diagnostics | script | 编辑后按扩展名选 linter（.ts→tsc, .py→ruff, .rs→cargo check） |
| 6.2 | Hook runtime profiles | config | `HARNESS_PROFILE=minimal\|standard\|strict` 一键切强度 |
| 6.3 | Session turn metrics | script | UserPromptSubmit + Stop 括号测量每轮耗时和 token 增量 |
| 6.4 | Test-before-commit gate | script | PreToolUse 拦截 `git commit`，测试不过则 deny |
| 6.5 | Atomic state writes | design | write-to-temp-then-rename 保证 crash 时不留半截 JSON |
| 6.6 | Session state hygiene | design | 定期清理 stale ralph.json / orphaned lock / empty session dir |

## 10 条设计原则

详见 [principles.md](principles.md)。

| # | 原则 | 一句话 |
|---|------|--------|
| M1 | Determinism over persuasion | hook 是确定的，prompt 是概率的 |
| M2 | Filesystem as coordination | 跨 agent/session 通信走磁盘文件 |
| M3 | Safety valves on every enforcement | 每个阻止机制必须有逃生条件 |
| M4 | Session-scoped isolation | 一个 session 一个目录，互不污染 |
| M5 | Fail-open on uncertainty | 状态不明确时放行（安全场景除外） |
| M6 | Proportional intervention | 简单任务不需要全套 hook |
| M7 | Observe before intervening | 先跑 tracker 再装 blocker |
| M8 | Explicit knowledge transfer | 决策写磁盘，不信 LLM 摘要 |
| M9 | Coordinator synthesizes | 协调者综合，不转发 |
| M10 | Honest limitation labeling | "未实现" 好过 "静默失效" |

## 不是什么

- **不是 agent 框架。** 不做模型调用，不管 prompt chain。只管 hook 和脚本。
- **不是任务调度。** 没有 DAG，没有 fan-in。多 agent 协调提供设计模式，不提供 runtime。
- **不是 prompt engineering。** Hook 是确定性机制。"不要重试超过 3 次" 写在 prompt 里是建议，写在 hook 里是系统级拦截。

## 测试

```bash
python3 -m pytest */tests/ -v   # 90 tests
```

依赖：`bash`、`jq`、`python3`、`pytest`

## 已知限制

- **Context 使用率**：transcript 不暴露 `context_window_size`，只能读 raw token 数，按 200K 窗口粗估
- **模型切换**：Hook 不能切换模型，Pattern 5.6 只能通过 additionalContext 建议 `[ADVISORY ONLY]`
- **Doubt gate 误报**：代码注释中的 "should be" 会匹配，用 one-shot guard 防死循环
- **Auto-compact circuit breaker**：连续 3 次失败后跳过 compact，依赖 compact 事件的 hook 不触发

## 蒸馏来源

| Source | 贡献 |
|--------|------|
| [harness-books](https://github.com/wquguru/harness-books) | Anthropic / OpenAI harness engineering 文章的结构化解读 |
| [claude-reviews-claude](https://github.com/openedclaude/claude-reviews-claude) | Claude Code 源码级架构分析（压缩、hook 协议、session 管理） |
| [ccunpacked.dev](https://ccunpacked.dev/) | Claude Code 工具全景和隐藏功能 |
| [claude-howto](https://github.com/luongnv89/claude-howto) | Hook 扩展点 API 教程 |
| Claude Code 源码 | 泄露的 TypeScript 源码直接阅读 |
| ClawHub harness skills | 社区贡献的实战 hook 脚本和踩坑经验 |

## License

MIT
