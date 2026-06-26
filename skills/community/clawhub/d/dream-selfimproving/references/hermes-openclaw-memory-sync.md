# OpenClaw ↔ Hermes 记忆同步

## 背景

Hermes 和 OpenClaw 各有独立的记忆系统：
- **Hermes**: `~/.hermes/memories/MEMORY.md` + `USER.md`
- **OpenClaw**: `~/.openclaw/memory/main.sqlite` (chunks 表，向量+RAG)

两者内容有重叠但不完全相同，存在信息不对称。

## 同步脚本

位置：`~/.hermes/scripts/sync_openclaw_memory.py`

功能：从 OpenClaw sqlite 提取 Hermes 没有的记忆，写入 Hermes 记忆文件。

```bash
# 预览同步内容（不写入）
python3 ~/.hermes/scripts/sync_openclaw_memory.py --dry-run

# 执行同步
python3 ~/.hermes/scripts/sync_openclaw_memory.py
```

### 同步逻辑

1. 读取 `~/.openclaw/memory/main.sqlite` 的 `chunks` 表（source='memory'）
2. 按 path 去重，取最新版本
3. 对每个文件类型（MEMORY.md、truth 文件等）提取内容
4. 检查 Hermes 记忆是否已包含该内容
5. 补充缺失章节到 `~/.hermes/memories/MEMORY.md` 和 `USER.md`

### 已同步内容（2026-04-29）

| 信息类型 | 来源 | 目标 |
|---------|------|------|
| 陛下开发的技能列表 | OpenClaw MEMORY.md | Hermes USER.md |
| OpenClaw-Admin 地址/账号 | OpenClaw MEMORY.md | Hermes USER.md |
| 技能积分榜系统配置 | OpenClaw MEMORY.md | Hermes USER.md |
| Cron 任务配置 | OpenClaw MEMORY.md | Hermes MEMORY.md |

## 局限性

1. **单向同步**：目前只从 OpenClaw → Hermes，没有反向同步
2. **手动触发**：需要手动运行脚本，未加入自动 cron
3. **仅同步 memory chunks**：不包括 OpenClaw 各 agent 的独立 sqlite（xiao.sqlite、main.sqlite 等）

## 改进方向

1. **定时自动同步**：加入每日 cron（建议在晚间蒸馏前执行）
2. **反向同步**：将 Hermes MEMORY.md 的重要更新写回 OpenClaw
3. **多 agent sqlite 整合**：读取 xiao.sqlite、content-reviewer.sqlite 等获取更多 agent 视角的记忆
4. **差异告警**：如果两边对同一事实的记录矛盾，告警通知
