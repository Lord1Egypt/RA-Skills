# Pattern 1.1: 持续执行循环（Ralph 模式）

## 问题

Claude Code agent 在复杂任务中经常"觉得自己做完了"就停了，实际上只完成了一部分。这在多文件修改、多步骤任务中尤其常见——agent 修完第一个文件后就发 `end_turn`，剩下的文件被遗忘。

## 原理

Claude Code 的 Stop hook 在 agent 尝试结束会话时触发。通过在 Stop hook 中返回 `{"decision":"block","reason":"..."}` 可以阻止终止并注入续航指令，让 agent 继续工作。

这个机制来自 OMC 的 `persistent-mode.mjs`——OMC 最核心的设计之一。整个 ralph/autopilot/team 持续执行系统都建立在这个 Stop hook 机制上。OMC 的实现中，Stop hook 按优先级检查 9 种模式（Ralph > Autopilot > Ultrapilot > Swarm > Ultrawork > UltraQA > Pipeline > Team > OMC Teams），每种模式有独立的状态文件和停止条件。

**仅适用于 interactive 模式**。Headless（`-p`）模式没有 Stop 事件循环，用 `--max-turns` 代替。

## 工作流程

```
Agent 尝试停止
  → Stop hook 触发
    → 读取 sessions/<session-id>/ralph.json
      → active=true 且 iteration < max?
        → 是: 阻止停止，注入"继续工作"，iteration++
        → 否: 放行停止
```

## 5 个安全阀（NEVER block）

Stop hook 在以下条件下 MUST 放行，不管 ralph 状态如何：

1. **Context 上限**：usage >= 95%。阻止会导致 context 溢出崩溃。Claude Code 内部在 `context_window` 和 `input_tokens` 比值达到 95% 时会触发紧急压缩（reactive compact），此时 Stop hook 必须让路。

2. **认证失败**：401/403 错误。Token 过期或权限被撤销，继续执行无意义。

3. **Cancel 信号**：带 TTL 的取消文件存在且未过期（见 Pattern 1.1-sub: Cancel TTL）。

4. **闲置超时**：2 小时无活动。防止 zombie 状态永远占用资源。OMC 使用 `STALE_STATE_THRESHOLD_MS = 7200000` 作为阈值。

5. **迭代上限**：达到 `max_iterations`。防止无限循环。OMC 默认 max=200（`OMC_SECURITY=strict` 时），到达上限后尝试 auto-extend +10 直到硬上限。

## 状态文件

```json
{
  "session_id": "my-bugfix-task",
  "active": true,
  "iteration": 3,
  "max_iterations": 50,
  "created_at": "2026-04-05T10:00:00Z",
  "last_checked_at": "2026-04-05T10:15:00Z"
}
```

存储在 `sessions/<session-id>/ralph.json`。所有状态文件使用 write-then-rename 原子写入防止并发损坏（见 Pattern 6.5）。

## 初始化与 Crash 恢复

```bash
# 初始化 ralph 状态（session-id, max-iterations）
scripts/ralph-init.sh my-task-001 50

# 如果检测到已有 active 状态（crash 恢复），自动从上次迭代继续
# 输出: "Resuming ralph from iteration 37 (previous state: active=true, reason=stale)"
```

`ralph-init.sh` 在初始化前检查是否存在残留状态。如果发现 `active: true` 或 `deactivation_reason: "stale"` 的状态文件，不会重置迭代计数器，而是从上次位置恢复。这解决了 agent 在第 37 轮 crash 后重启从第 0 轮开始的问题。

## settings.json 配置

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "bash /path/to/execution-loop/scripts/ralph-stop-hook.sh"
      }]
    }]
  }
}
```

## 三种 Stop Hook 实现

### 模式 A: Shell 脚本（已实现，`scripts/ralph-stop-hook.sh`）

基于 JSON 状态文件的确定性检查。读 stdin（Claude Code hook 协议），读状态文件，输出 block/continue JSON。

- **优点**：快速、零 API 成本、可预测
- **缺点**：只能做迭代计数检查，无法判断任务是否"语义上完成"

### 模式 B: Prompt-type hook（推荐用于高价值任务）

用 LLM 本身判断任务是否完成。Claude Code 支持 `type: "prompt"` 的 hook，hook 内容作为 prompt 发给模型，模型返回结构化 JSON 决策。

```json
{
  "hooks": [{
    "type": "prompt",
    "prompt": "检查当前任务是否已全部完成。评估标准：1) 所有需要修改的文件已保存 2) 测试已通过 3) 无遗留 TODO/FIXME 4) 改动覆盖了原始需求的所有要点。如果未完成，返回 {\"decision\":\"block\",\"reason\":\"未完成：<具体缺失项>\"}；如果已完成，返回 {\"decision\":\"allow\"}。"
  }]
}
```

- **优点**：能捕捉"修了 bug 但没写测试"、"改了 3 个文件但还有 2 个没改"等语义级未完成状态
- **缺点**：每次 Stop 都消耗一次 API 调用

### 模式 C: Agent-type hook（最强，用于关键任务）

生成一个有完整工具访问权（Read、Grep、Bash）的 subagent 做多步验证：

```json
{
  "hooks": [{
    "type": "agent",
    "agent": "验证当前任务完成质量：1) 读取所有修改的文件确认改动正确 2) 运行 grep 检查无遗留 TODO/FIXME 3) 如果有测试文件，运行 bash 确认测试通过。返回结构化验证结果。"
  }]
}
```

- **优点**：能实际读文件、跑测试、检查编译
- **缺点**：最慢、消耗最多 token
- **建议**：配合 `maxTurns: 10` 限制验证 agent 的执行轮数，防止验证本身无限循环

## Block 消息设计

OMC 的 Ralph 注入的 block 消息很简单："Work is NOT done. Continue working."。根据 prompt-hardening 的 P5（反推理阻断）原则，更有效的消息应该预判 agent 的"合理化"倾向：

```
[RALPH LOOP 5/50] Task is NOT done.
Do NOT rationalize that "the remaining work can be done in a follow-up."
Do NOT claim completion with caveats.
Check your original task description and verify EVERY requirement is met.
Continue working on the original task.
```

## OMC 内部实现参考

OMC 的 `persistent-mode.mjs` 有几个值得注意的设计决策：

1. **状态闲置检查**：`STALE_STATE_THRESHOLD_MS = 7200000`（2 小时），超过此时间的状态被视为 zombie
2. **Auto-extend**：到达 `max_iterations` 后自动 +10 而非直接停止，直到硬上限（strict 模式 200）
3. **Cancel 信号 TTL**：`CANCEL_SIGNAL_TTL_MS = 30000`（30 秒），过期信号自动忽略
4. **Context-aware 放行**：读取 transcript 尾部 4KB 估算 context 使用率，>= 95% 时无条件放行
5. **优先级排序**：9 种模式按优先级检查，Ralph 最高，确保不同模式不冲突
