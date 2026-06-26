# session-cleaner

一个用于清理 OpenClaw 无用会话的 Skill。自动清理过期的 session 文件和 `sessions.json` 中的无效条目，保持会话列表整洁。

## 功能

- 清理 `sessions.json` 中的无效条目（已删除文件但仍存在的"幽灵"记录）
- 删除孤立的 `.jsonl`、`.trajectory.jsonl`、`.checkpoint.jsonl` 文件
- 保留正在运行（`running`）的会话和各 Agent 的 main session
- 自动识别 `main` Agent 是否存在并做相应处理
- 支持跨平台（任何安装了 OpenClaw 的机器均可使用）

## 安装

### 方式一：通过 OpenClaw Skill 管理器安装

```bash
openclaw skills install /path/to/session-cleaner.skill
```

### 方式二：手动安装

将 `session-cleaner` 文件夹复制到 OpenClaw 的 skills 目录：

```bash
cp -r session-cleaner ~/.openclaw/skills/
```

## 使用方法

在 OpenClaw 中直接告诉阿喵：

- "清理会话"
- "删除旧 session"
- "整理会话列表"

阿喵会自动加载 `session-cleaner` 技能并执行清理。

## 工作原理

### 会话存储结构

OpenClaw 的会话数据存储在 `$OPENCLAW_HOME/agents/<agent-id>/sessions/` 目录下：

```
sessions/
├── sessions.json          # 会话索引（会话元数据）
├── <uuid>.jsonl           # transcript 文件（实际消息记录）
├── <uuid>.trajectory.jsonl  # 任务轨迹文件
└── <uuid>.checkpoint.jsonl  # 检查点文件
```

### 保留策略

| 类型 | 是否保留 |
|------|---------|
| `running` 状态的会话 | ✅ 是 |
| 各 Agent 的 main session | ✅ 是 |
| `done` / `timeout` / `failed` 的子 Agent | ❌ 否 |
| `.trajectory.jsonl` | ❌ 否 |
| `.checkpoint.jsonl` | ❌ 否 |
| `main` Agent 的所有会话（若 main 不存在）| ❌ 否 |

### 清理流程

1. 扫描所有 Agent 的 `sessions.json`
2. 识别可清理的条目（保留 running + main session）
3. 直接编辑 `sessions.json` 删除无效条目
4. 删除孤立的 transcript / trajectory / checkpoint 文件
5. 重启 Gateway 使变更生效
6. 验证清理结果

## 注意事项

- **不要删除 running 状态的会话**——正在进行的工作会丢失
- 建议在清理前备份：`cp sessions.json sessions.json.bak`
- 清理完成后需重启 Gateway，否则 Control UI 可能仍显示旧数据
- 如果 `sessions.json` 已为空但 Control UI 仍显示旧数据，重启 Gateway 即可

## 文件结构

```
session-cleaner/
├── SKILL.md    # 技能说明文件
└── README.md   # 本说明文档
```

## 适用场景

- 控制面板会话列表变得混乱，大量过期条目
- 磁盘空间被大量 `.trajectory.jsonl` 文件占用
- `main` Agent 被删除后其旧会话仍显示在列表中
- 定期维护，保持 OpenClaw 运行状态整洁

## License

MIT