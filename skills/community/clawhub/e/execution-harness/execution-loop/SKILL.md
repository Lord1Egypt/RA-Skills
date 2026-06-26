---
name: execution-loop
version: 2.0.0
description: Agent 执行循环控制。当 agent 提前停止、偏离任务、或在 headless 模式下需要执行控制时使用。不适用于工具重试（用 tool-governance）。参见 context-memory（阶段边界 handoff）、quality-verification（编辑后检查）。
license: MIT
triggers:
  - agent keeps stopping
  - ralph
  - persistent execution
  - 不要停
  - doubt gate
  - task completion
  - headless mode
  - agent drifts
  - adaptive complexity
author: OpenClaw Team
---

# Execution Loop

控制 agent 的执行循环：阻止提前停止、检测任务完成、防止任务漂移。

## When to Use

- Agent 只完成一部分就停了 → Ralph persistent loop
- Agent 说"可能"就声称完成 → Doubt gate
- 长 session 中偏离原始任务 → Drift re-anchoring
- 有明确任务清单 → Task completion verifier
- 用 `-p` headless 模式 → Headless execution control

## When NOT to Use

- 工具反复失败 → 用 `tool-governance`
- 上下文快用完 → 用 `context-memory`
- Session 挂死 → 用 `error-recovery`

---

## Patterns

| # | Pattern | Type | Description |
|---|---------|------|-------------|
| 1.1 | Ralph persistent loop | [script] | Stop hook 在 agent 尝试 end_turn 时检查 `ralph.json` 状态，未达 max 则 block 并注入续航指令。核心保障是 5 个安全阀（context >=95%、401/403、cancel TTL、闲置 2h、迭代上限），安全阀优先级高于一切 block 逻辑——context 即将溢出时 Ralph 必须让路，否则 session 崩溃。支持 shell/prompt/agent 三种 hook 实现，高价值任务用 agent-type 做语义级完成度验证。 → [详见](references/ralph.md) |
| 1.2 | Doubt gate | [script] | Strip 代码块和引用后扫描 agent 回复中的 hedging 词（"likely""maybe""可能""应该是"等），命中则 block 并要求提供日志、测试结果等具体证据。用 `$TMPDIR/doubt-gate-<session>` 守卫文件做单轮去重——同一轮触发过一次后无条件放行，防止 agent 永远无法停止。与 Ralph 正交叠加：Ralph 管"别停"，Doubt Gate 管"别含糊地停"。 → [详见](references/doubt-gate.md) |
| 1.3 | Adaptive complexity triage | [design] | 执行前根据文件数、安全/迁移关键词做 triage，将任务分为 Trivial→Express 到 Critical→Full+Gate 五档，每档启用不同的 hook 组合。关键约束：triage 不确定时默认 Standard 而非 Express，因为 Express 跳过验证——安全修复被误判为 Trivial 会不经验证直接提交。文件计数是极简启发式，生产环境建议用一次 Haiku 调用替代。 → [详见](references/adaptive-complexity.md) |
| 1.4 | Task completion verifier | [script] | Stop hook 读取 `.harness-tasks.json`（`{tasks: [{name, done}]}`），存在 `done: false` 条目则 block 并将未完成项注入 reason。与 Ralph 互补：Ralph 只做迭代计数，Task Completion 提供语义级的"为什么不能停"。确定性校验、零 API 成本，但 agent 可能只标记完成而实际没做好，需配合 quality-verification 二次验证。 → [详见](references/task-completion.md) |
| 1.5 | Drift re-anchoring | [script] | 每 N 轮（默认 10）将原始任务描述通过 `hookSpecificOutput.additionalContext` 重新注入对话，作为防漂移锚点。在 Ralph 持续执行中尤其必要——agent 不停意味着 drift 没有天然修正点，第 5 轮开始"顺手"重构不相关代码，第 10 轮已经在优化 CI 配置。与 Ralph、Task Completion 三者各管一个维度：别停 / 为什么不能停 / 别跑偏。 → [详见](references/drift-reanchor.md) |
| 1.6 | Headless execution control | [config] | `-p` 模式没有 Stop 事件循环，Ralph 不生效。替代方案是三维控制：`--max-turns` 限轮数，prompt 结构化（系统指令放前 ~2000 token 利用 prefix cache），budget 注入让 agent 感知资源约束做优先级决策。Pipeline 场景每阶段告知当前位置和剩余预算。 → [详见](references/headless-config.md) |
| 1.7 | Iteration-aware messaging | [design] | Ralph 的 block 消息如果每次相同，agent 会进入 compliance mode——表面继续实际反复生成"我已完成大部分"的变体。解法是按迭代阶段动态切换消息角度：早期(1-5)方向引导，中期(6-15)反合理化要求逐条对照，后期(16-30)反循环鼓励换方法，收尾(30+)切换优先级做 graceful handoff。基于 prompt-hardening P5 反推理阻断原则。 → [详见](references/iteration-aware-messaging.md) |

扩展模式（跨 turn 状态对象、多层停止条件、三维预算约束、流式工具执行）→ [详见](references/extended-patterns.md)。Cancel 信号 TTL 机制 → [详见](references/cancel-ttl.md)。

## Scripts

| 脚本 | Hook 类型 | 功能 |
|------|----------|------|
| `ralph-stop-hook.sh` | Stop | 阻止提前停止，5 安全阀 |
| `ralph-init.sh <id> [max]` | CLI | 初始化持续执行 |
| `ralph-cancel.sh <id>` | CLI | 发送取消信号 |
| `doubt-gate.sh` | Stop | 检测 hedging words |
| `task-completion-gate.sh` | Stop | 读 .harness-tasks.json |
| `drift-reanchor.sh` | Stop | 每 N 轮注入原始任务提醒 |

## Workflow

```
任务到达
  │
  ├─ Interactive 模式？
  │   │
  │   ├─ 是 ──→ 复杂度 triage（Pattern 1.3）
  │   │         │
  │   │         ├─ Trivial/Low ──→ Express/Light 模式
  │   │         │   不启用 Ralph，agent 完成即停。
  │   │         │   判断不确定？→ 走 Standard，Express 跳过验证不可兜底。
  │   │         │
  │   │         └─ Medium+ ──→ Standard/Full 模式
  │   │             │
  │   │             ├─ 1. ralph-init.sh <id> [max]
  │   │             │   有残留状态？从上次迭代恢复，不重置计数器。
  │   │             │
  │   │             ├─ 2. 按复杂度启用 hook 组合
  │   │             │   Standard: Ralph + Context 估算
  │   │             │   Full: + Handoff + Hook Bracket + Post-Edit 诊断
  │   │             │   Critical: + Agent-type 验证门禁
  │   │             │
  │   │             └─ 3. Agent 执行 → 尝试停止 → Stop hook 链
  │   │                 │
  │   │                 ├─ [最高优先级] 安全阀检查
  │   │                 │   context >= 95%? → 放行（阻止会导致溢出崩溃）
  │   │                 │   401/403 认证失败? → 放行（继续执行无意义）
  │   │                 │   cancel 信号存在且 TTL 未过期? → 放行
  │   │                 │   闲置 > 2h? → 放行（防 zombie）
  │   │                 │   迭代 >= max? → 放行
  │   │                 │   ※ 安全阀先于一切 block 逻辑执行，顺序固定
  │   │                 │
  │   │                 ├─ Doubt gate（Pattern 1.2）
  │   │                 │   回复含投机语言? → block，要求证据
  │   │                 │   本轮已触发过? → 放行（守卫去重）
  │   │                 │
  │   │                 ├─ Task completion（Pattern 1.4）
  │   │                 │   .harness-tasks.json 有未完成项? → block，注入缺失项
  │   │                 │
  │   │                 ├─ Ralph 迭代检查（Pattern 1.1）
  │   │                 │   active=true 且 iteration < max? → block
  │   │                 │   注入迭代感知消息（Pattern 1.7）
  │   │                 │
  │   │                 ├─ Drift re-anchor（Pattern 1.5）
  │   │                 │   每 N 轮注入原始任务提醒（不 block，仅注入 context）
  │   │                 │
  │   │                 └─ 所有检查通过 → 放行停止
  │   │
  │   └─ 否（Headless `-p`）──→ 三维控制（Pattern 1.6）
  │       --max-turns 限轮数（简单 10-20 / 中等 30-50 / 复杂 80-120）
  │       prompt 结构化利用 prefix cache
  │       budget 注入让 agent 感知剩余资源
  │       第 80% 轮次时开始收尾，写 handoff 文档
```

<example>
场景：7 文件 API 重构

用户：「把 user-service 的 7 个 endpoint 从 REST 迁移到 gRPC」
→ Triage: High（7 文件 + 架构变更）→ Full 模式
→ ralph-init.sh api-migration 50

Agent 改完 1 个 endpoint → 停 → Ralph block:
  「[RALPH 1/50] 检查任务清单，标记已完成项，继续下一项。」
Agent 改完 3 个 → 停 → Task completion block:
  「未完成项: endpoint-4, endpoint-5, endpoint-6, endpoint-7」
Agent 改完全部 7 个 → 停 →
  Doubt gate 通过（无投机语言）→ Task completion 通过（全部 done）→ Ralph 放行
实际迭代: 12/50，自然完成。
</example>

<anti-example>
场景：拼写修复误用 Ralph

用户：「README 里 'recieve' 改成 'receive'」
错误：ralph-init.sh typo-fix 50 → 改完 1 行被 Ralph block → 被迫"寻找更多错误" → 引入无关改动
正确：Triage → Trivial → Express → 不启 Ralph → 改完即停
</anti-example>

## Output

| 产物 | 路径 | 说明 |
|------|------|------|
| Ralph 状态文件 | `sessions/<session-id>/ralph.json` | 记录 active、iteration、max_iterations、时间戳。原子写入（write-then-rename） |
| Doubt gate 守卫文件 | `$TMPDIR/doubt-gate-<session-id>` | 防止 doubt gate 同一轮重复触发。临时文件，触发后创建，放行后删除 |
| 任务清单 | `.harness-tasks.json` | 任务 checklist，格式 `{tasks: [{name, done}]}`。agent 完成子任务后标记 `done: true` |

## Usage

在 `.claude/settings.json` 中配置 Stop hook：

```jsonc
{
  "hooks": {
    "Stop": [
      // Ralph 持续执行（Pattern 1.1）
      {
        "hooks": [{
          "type": "command",
          "command": "bash ralph-stop-hook.sh"
        }]
      },
      // Doubt gate（Pattern 1.2）
      {
        "hooks": [{
          "type": "command",
          "command": "bash doubt-gate.sh"
        }]
      },
      // Task completion（Pattern 1.4）
      {
        "hooks": [{
          "type": "command",
          "command": "bash task-completion-gate.sh"
        }]
      }
    ]
  }
}
```

初始化和取消 Ralph：
```bash
# 启动持续执行（50 轮上限）
bash ralph-init.sh api-migration 50

# 取消持续执行
bash ralph-cancel.sh api-migration
```

Hook 输出格式（ralph-stop-hook.sh stdout）：
```json
{"decision": "block", "hookSpecificOutput": {"reasonForBlocking": "[RALPH 3/50] 检查任务清单，标记已完成项，继续下一项。"}}
```

安全阀在 block 之前检查，确保不会阻止必要的停止：
```json
{"decision": "allow", "hookSpecificOutput": {"reasonForAllowing": "context >= 95%, 必须放行避免溢出"}}
```

## Related

| Skill | 关系 |
|-------|------|
| `tool-governance` | 上游：提供工具错误数据。工具连续失败时由 tool-governance 处理，不属于 execution-loop 范围 |
| `context-memory` | 互补：阶段边界时写 handoff document。Ralph 到达 max 或 context 接近上限时，应触发 context-memory 保存决策 |
| `quality-verification` | 下游：agent 完成编辑后由 quality-verification 做 post-edit 检查（lint、type check、测试） |
