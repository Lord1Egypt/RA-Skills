# cleanup-sessions 技能

清理已中止的子 agent 会话文件。

## 安装

### 从 ClawHub 安装（推荐）

```bash
clawhub install cleanup-sessions
```

### 本地使用

技能已在本地的：
```
~/.openclaw/workspace/skills/cleanup-sessions/
```

## 使用方式

### 方式 1：对话清理（推荐）

在对话中直接说：
- "清理已中止的子 agent 会话"
- "删除 abort 的会话文件"
- "清理备份文件"
- "清理 .deleted 和 .reset 文件"
- "完整清理 sessions 目录"

助理会自动：
1. 调用 `sessions_list()` 获取会话列表
2. 过滤出 `abortedLastRun: true` 的子 agent 会话
3. **应用 48 小时保护**（跳过近期会话）
4. 扫描 `.deleted` 和 `.reset` 备份文件
5. 展示待删除文件列表（含大小、最后更新时间）
6. 确认后执行删除

### 方式 2：命令行脚本

```bash
# 清理备份文件（快速释放空间）
cd ~/.openclaw/agents/main/sessions
rm -f *.jsonl.deleted.*
find . -name "*.jsonl.reset.*" -mtime +7 -delete

# 预览模式（不删除）
bash ~/.openclaw/workspace/skills/cleanup-sessions/cleanup.sh --dry-run

# 交互模式（确认后删除）
bash ~/.openclaw/workspace/skills/cleanup-sessions/cleanup.sh
```

## 文件结构

```
cleanup-sessions/
├── SKILL.md      # 技能定义
├── cleanup.sh    # 命令行脚本
└── README.md     # 使用说明
```

## 安全特性

- ✅ 只删除子 agent 会话（key 包含 `subagent`）
- ✅ 只删除已中止的会话（`abortedLastRun: true`）
- ✅ 删除前展示文件列表和大小
- ✅ 需要用户确认
- ✅ 同步清理 `sessions.json` 索引（保持数据一致性）
- ✅ 备份文件分类清理（.deleted 全删，.reset 保留 7 天）
- ✅ **48 小时保护**：不删除近期会话（防止误删正在使用的会话）

## 维护建议

### 定期清理

建议每周清理一次，可通过 heartbeat 自动提醒：

```markdown
# HEARTBEAT.md

- [ ] 检查并清理已中止的子 agent 会话
- [ ] 清理 7 天前的备份文件（.deleted 和 .reset）
```

### 备份文件说明

| 类型 | 说明 | 清理策略 |
|------|------|----------|
| `.jsonl.deleted.*` | 会话删除前的备份 | 全部删除 |
| `.jsonl.reset.*` | 会话重置/压缩前的备份 | 保留 7 天 |

### 空间监控

如果 sessions 目录占用超过 1 GB，建议立即清理：

```bash
du -sh ~/.openclaw/agents/main/sessions/
```
