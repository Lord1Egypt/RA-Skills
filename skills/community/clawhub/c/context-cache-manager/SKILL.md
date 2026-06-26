# Context Cache Manager

>
> fork-safe上下文克隆 + 智能压缩 + 快速恢复
> 参考Claude Code fork设计和Context缓存机制

## 背景问题

OpenClaw原生上下文管理：
- **fork时上下文丢失** — 子Agent无法继承父进程关键状态
- **历史消息膨胀** — 长时间对话导致token爆炸
- **session恢复慢** — 重启后丢失工作上下文
- **内容替换状态乱序** — 多Agent同时修改导致冲突

**根因**：缺乏Claude Code的fork-safe三剑客克隆机制

## 解决方案

### Fork-Safe三剑客（必须克隆）

参考Claude Code原始设计，fork时必须克隆：

```typescript
// 父进程 → 子进程
{
  contentReplacementState: parent.contentReplacementState.clone(),  // 内容替换状态
  renderedSystemPrompt: parent.renderedSystemPrompt,                // 渲染后的system提示
  messages: parent.messages.clone()                                // 消息历史
}
```

### 智能压缩策略

```
完整消息历史 (100条+) 
    ↓ 压缩
保留：
  - 所有system消息（完整）
  - 最近20条消息（完整）
  - 更早消息 → 摘要标记
    [Compressed 80 older messages]
    ↓
压缩后 ~25条等效消息
```

### Session生命周期

```
[ACTIVE] ──fork──> [FORKED] (父) + [ACTIVE] (子)
   │
   ├──compact──> [COMPACTED]
   │
   └──archive──> [ARCHIVED]
           │
           └──cleanup──> deleted (24h后)
```

## 使用方式

### Python API

```python
from context_cache_manager import ContextCacheManager, fork_context

# 方式1：面向对象
manager = ContextCacheManager("session-001")

# 捕获当前上下文
manager.capture(
    system_prompt="You are OpenClaw agent...",
    messages=[...],
    content_replacement_state={"replaced": [...]},
    rendered_system_prompt="Rendered prompt with context..."
)

# 快速恢复
restored = manager.restore()
print(f"Restored {len(restored.messages)} messages")

# Fork到子session
child = manager.fork("child-session-002")
assert child.content_replacement_state == parent.content_replacement_state

# 方式2：便捷函数
child = fork_context("parent-id", "child-id")
```

### 压缩效果

| 原始消息数 | 压缩后 | 压缩率 | 等效token |
|-----------|--------|--------|----------|
| 50 | 25 | 50% | ~60% |
| 100 | 25 | 75% | ~70% |
| 200 | 25 | 87.5% | ~75% |

### Skill集成

```yaml
whenToUse: |
  spawn子Agent前捕获父context
  session恢复时快速重建
  长时间对话后压缩上下文
permissions:
  - file:write (缓存目录)
  - file:read (恢复缓存)
  - memory:manage
hooks:
  before_spawn: capture_context
  after_spawn_complete: fork_context
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MAX_HISTORY_LENGTH` | 50 | 最大保留消息数 |
| `MAX_CACHE_AGE_HOURS` | 24 | 缓存过期时间 |
| `CACHE_DIR` | `tmp/context-cache/` | 缓存目录 |
| `format` | pickle+gzip | 高效序列化 |

## 与AgentConcurrency配合

```python
from agent_concurrency_controller import spawn_agent_safe
from context_cache_manager import ContextCacheManager

# 1. 捕获父上下文
parent_ctx = ContextCacheManager("main-session")
parent_ctx.capture(system_prompt, messages)

# 2. 安全spawn（自动fork上下文）
result = spawn_agent_safe(
    task="子任务",
    agent_type="researcher",
    context_manager=parent_ctx  # 自动fork
)

# 3. 子Agent继承完整上下文
```

## 日志审计

### 缓存日志 (`logs/context-cache.log`)
```
[2026-04-03 15:40:00] CAPTURE: session-001 | 15000_chars | compressed: true
[2026-04-03 15:40:05] FORK: session-001 -> child-002 | cloned 3 fields
[2026-04-03 15:45:00] COMPACT: session-001 | 100->25 messages | saved 65%
[2026-04-03 16:00:00] RESTORE: session-001 | loaded from cache
```

## 最佳实践

1. **spawn前capture** — 确保可fork
2. **长对话后compact** — 防止token爆炸
3. **定期cleanup** — 删除过期缓存
4. **immutable fork** — 子进程不修改父状态

## 关联

- 并发控制：`skills/agent-concurrency-controller/`
- 结果控制：`skills/tool-result-size-controller/`
- 安全编辑：`skills/safe-file-editor/`
- 架构参考：`memory/learnings/claude-code-architecture-2026-04-03.md`

## 版本

- **v1.0.0** (2026-04-03): 初始实现，fork-safe三剑客克隆+智能压缩
