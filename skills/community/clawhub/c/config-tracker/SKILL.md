# Config Tracker Skill

自动追踪并提交 OpenClaw 配置文件和关键 markdown 文件的变更。

## 功能

- **自动版本控制**：每次对话轮次开始时自动检查并提交文件变更
- **双仓库管理**：分别管理 `~/.openclaw/` 和 workspace 目录
- **零手动操作**：无需手动执行 git 命令，所有提交自动完成
- **可配置**：可自定义追踪的文件列表和提交信息

## 追踪的文件

### Workspace 目录

- `AGENTS.md` — Agent 工作区配置
- `USER.md` — 用户信息
- `SOUL.md` — Agent 身份设定
- `MEMORY.md` — 长期记忆
- `TOOLS.md` — 工具配置
- `HEARTBEAT.md` — 心跳任务配置
- `IDENTITY.md` — Agent 身份

### OpenClaw 配置

- `~/.openclaw/openclaw.json` — 主配置文件

## 触发时机

使用 `before_prompt_build` hook，每次对话轮次开始时自动检查并提交变更。

## 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `enabled` | `true` | 启用/禁用追踪器 |
| `workspaceFiles` | `["AGENTS.md", "USER.md", ...]` | 要追踪的 workspace 文件列表 |
| `openclawConfig` | `~/.openclaw/openclaw.json` | OpenClaw 配置文件路径 |
| `commitMessagePrefix` | `"auto: track config changes"` | 提交信息前缀 |
| `gitUserName` | `"OpenClaw Bot"` | Git 用户名 |
| `gitUserEmail` | `"openclaw@localhost"` | Git 用户邮箱 |

## 安装

将 `config-tracker` 目录复制到你的 skills 目录：

```bash
cp -r config-tracker/ /Volumes/File/OpenClaw/workspace/skills/
```

然后重启 OpenClaw gateway 使其生效。

## 工作原理

1. 每次对话轮次开始时（`before_prompt_build` hook），插件检查配置文件是否有变更
2. 使用 `git status --porcelain` 检测未提交的变更
3. 若有变更，自动执行 `git add <file>` + `git commit -m "auto: track config changes [timestamp]"`
4. 提交信息包含时间戳，便于追溯

## 注意事项

- 首次运行时会自动初始化 git 仓库
- 频繁修改配置文件（如 Doctor 自动修改）会产生大量提交，这是预期行为
- 使用 `git log` 可以查看完整的历史变更
- 提交冷却是 5 秒，防止短时间内多次提交
