# Pattern 3.2: Compaction 前记忆提取（Save Before Delete）

## 问题

Claude Code 的 auto-compact 在 context 接近上限时自动触发。压缩会丢弃旧消息，其中可能包含重要的设计决策和发现。

## 原理

利用 Stop hook 定期提取关键信息到磁盘。注意：Claude Code **没有** PreCompact hook event。实际实现通过 Stop hook 每 N 轮触发一次快照，作为压缩前的预防性知识保存。Claude Code 内部有 `buildExtractAutoOnlyPrompt` 和 `buildExtractCombinedPrompt`，但这些是内部 API，不暴露给外部 hook。

## 与 Handoff 文档的区别

| | Handoff 文档 (Pattern 3.1) | Compaction 提取 (Pattern 3.2) |
|---|---|---|
| 触发时机 | 阶段结束时（主动） | 压缩触发时（被动） |
| 触发者 | Agent 自行写入 | Stop hook 定期触发 |
| 内容控制 | 完全由 agent 决定 | 由脚本自动快照 |
| 可靠性 | 依赖 agent 遵守指令 | 系统级定期保证 |

两者互补：handoff 是计划内的上下文传递，compaction 提取是应急的知识抢救。

## 实现

settings.json 中配置 Stop hook（每 N 轮触发一次快照）：

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "bash /path/to/context-memory/scripts/compaction-extract.sh",
        "async": true
      }]
    }]
  }
}
```

通过 `COMPACTION_EXTRACT_INTERVAL` 环境变量控制快照频率（默认每 15 轮）。

> **注意**: Claude Code 没有 PreCompact hook event。此脚本通过定期快照实现预防性知识保存，而非精确的压缩前拦截。

## Claude Code 的 Memory Extraction 机制

Claude Code 内部有两种 extraction prompt builder：

- `buildExtractAutoOnlyPrompt`：只提取 private memory（用户偏好、工作习惯）
- `buildExtractCombinedPrompt`：根据内容敏感性路由到 private 或 team scope

提取发生在压缩的同时（并行），提取结果写入 memdir 的 Markdown 文件。Memory taxonomy 包含 4 种类型：user（个人偏好）、feedback（纠正/表扬）、project（架构/目标）、reference（外部文档/流程）。
