## 八卦记忆维护

定期（建议每周或每次心跳）执行：

- 检查 `memory/bagua/li/` 中超过 7 天的条目，移入 `memory/bagua/gen/`
- 压缩 `memory/bagua/gen/` 中超过 30 天的条目为摘要
- 更新 `MEMORY.md` 索引
- 清理无引用的孤立记忆
