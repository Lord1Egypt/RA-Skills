# Pattern 3.1: Handoff 文档（上下文存活）

## 问题

Claude Code 的 context window 有限。长任务中会触发 auto-compact（4 级压缩：MicroCompact → Session Memory → Full Compact → Reactive Compact），压缩后关键设计决策、排除过的方案、已识别的风险都会丢失。

## 原理

在阶段结束或 context 压缩前，将关键信息写入磁盘文件。压缩后的 agent 可以通过读取这些文件恢复上下文。这比依赖 Claude Code 的压缩摘要更可控——你决定保留什么，而不是让压缩算法决定。

来自 OMC 的 `.omc/handoffs/<stage-name>.md` 机制——每个 team pipeline 阶段产出一份 handoff 文档，包含 Decided/Rejected/Risks/Files/Remaining 五段。

## 文档结构（5 个必要段落）

```markdown
# Handoff: <stage-name>

## Decided
- 选择 Redis 作为缓存方案，因为项目已有 Redis 依赖，无需新增基础设施
- 使用 LRU 策略，TTL 设为 5 分钟

## Rejected
- 排除 Memcached：团队无运维经验
- 排除本地文件缓存：不支持多实例部署

## Risks
- Redis 单点故障需要 Sentinel（当前未配置）
- 缓存穿透风险：高频查询的 key 需要布隆过滤器

## Files Modified
- src/cache/redis_client.py — 新建，Redis 连接池封装
- src/api/handlers.py:45-67 — 添加缓存查询层
- tests/test_cache.py — 缓存命中/未命中/过期测试

## Remaining
- Sentinel 配置（下个迭代）
- 缓存预热逻辑
- 监控指标接入
```

## 存储位置

```
sessions/<session-id>/handoffs/
  stage-1-plan.md
  stage-2-implement.md
  stage-3-verify.md
  pre-compact.md          ← 压缩前自动抢救（见 Pattern 3.2）
```

## 注入方式

在 agent 的 prompt 尾部追加：

```
在完成当前阶段前，将关键决策写入 handoff 文档：
sessions/<session-id>/handoffs/stage-<当前阶段>.md
必须包含 5 个段落：Decided / Rejected / Risks / Files Modified / Remaining
```

下一阶段的 agent 启动时，通过 UserPromptSubmit hook 或 prompt 注入最新的 handoff 文档。配合 `once: true` 标记确保只注入一次（见 Pattern 2.5）。

## 为什么不依赖 Claude Code 的内置压缩

Claude Code 的 Full Compact 使用 LLM 生成 9 段式结构化摘要，质量不错但有两个问题：

1. **摘要内容由 LLM 决定**，你无法控制保留什么
2. **使用 `<analysis>` scratchpad 提高摘要质量但 strip 后注入**（chain-of-thought 不进入压缩后的 context），意味着推理过程丢失

Handoff 文档让你显式控制保留的信息，和内置压缩互补而非替代。

## 已知局限

- Handoff 文档可能跨阶段产生矛盾（stage-2 推翻了 stage-1 的决策但没更新 stage-1 的 handoff）
- 过多阶段后，累积的 handoff 内容本身成为 context 负担
- Agent 可能不遵守写 handoff 的指令——这是概率性的，不是系统保证

用 Pattern 3.3（记忆合并）可以部分缓解 staleness 和碎片化问题。

## Claude Code 的 4 级压缩（背景知识）

> 以下信息基于 Claude Code 源码分析（v2.1.88），内部实现可能随版本变化。

| 级别 | 方法 | 压缩率 | 成本 |
|------|------|--------|------|
| MicroCompact | 手术式移除旧 tool results（8 种特定工具类型） | 10-50K tokens | 零（无 LLM 调用） |
| Session Memory | 用预建的背景摘要替换旧消息 | 60-80% | 零（摘要由后台 agent 维护） |
| Full Compact | LLM 生成 9 段结构化摘要 | 80-95% | 一次 API 调用 + 全缓存失效 |
| Reactive Compact | API 返回 413 后的紧急压缩 | 可变 | 应急措施 |

Handoff 文档在任何级别的压缩中都不会丢失——因为它在磁盘上，不在 context 里。
