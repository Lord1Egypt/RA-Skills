# Filesystem Working Memory

## Problem

Agent 在长会话中积累的决策、计划、中间结论只存在于 context window 中。一旦 compact 或 session 结束，这些信息丢失。下次 compact 后 agent 不记得"为什么选了方案 B 而不是方案 A"，导致重复决策或矛盾操作。

## Solution

用 `.working-state/` 目录作为 agent 的"外部工作记忆"。包含两个核心文件：`current-plan.md`（当前执行计划，agent 随时读写）和 `decisions.jsonl`（决策日志，append-only）。Agent 在做出关键决策时写入 decisions.jsonl，在更新计划时覆写 current-plan.md。Compact 后 agent 通过读取这些文件恢复状态。

## Implementation

1. 任务启动时创建 `.working-state/` 目录

```bash
mkdir -p .working-state
```

2. `current-plan.md`：Agent 的当前执行计划

```markdown
# 当前计划（更新于 iteration 12）

## 已完成
- [x] 分析 parser.ts 结构
- [x] 添加新 AST 节点类型

## 进行中
- [ ] 更新 visitor pattern

## 待做
- [ ] 写测试
- [ ] 更新文档
```

3. `decisions.jsonl`：每行一个决策记录

```jsonl
{"ts":"2026-04-06T10:00:00Z","decision":"选择 visitor pattern 而非 switch-case","reason":"可扩展性，未来新增节点类型不需要改核心逻辑","alternatives":["switch-case (更简单但不可扩展)"]}
{"ts":"2026-04-06T10:15:00Z","decision":"parser 错误用 Result 类型而非 throw","reason":"调用方可以 pattern match，不会遗漏错误处理"}
```

4. Post-compact 恢复：在 CLAUDE.md 或 system prompt 中指示 agent：

```
每次 compact 后，先读取 .working-state/current-plan.md 和 .working-state/decisions.jsonl 恢复上下文。
```

5. 可选的辅助文件：
   - `scratch.md`：临时笔记，不保证存活
   - `blocked.md`：当前阻塞项和原因

## Tradeoffs

- **Pro**: 信息在 compact、crash、session 切换中存活
- **Pro**: 决策日志让 agent（和人类）理解历史推理过程
- **Con**: Agent 需要"记得"写入这些文件——需要在 prompt 中明确要求
- **Con**: 文件读写消耗 context token（但远小于丢失信息后的重复探索）

## Source

Claude Code 的 CLAUDE.md persistent memory 机制的扩展。OMC 的 handoff 文档系统。Last Whisper Dev 的 "filesystem as memory" 实践。
