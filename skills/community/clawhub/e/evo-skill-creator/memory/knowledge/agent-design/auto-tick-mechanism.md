# 自动 Tick 机制——Skill 定期自动触发

> 学习日期：2026-03-26
> 更新：2026-03-26（修正——移除未验证内容，基于实际可用能力）

## 核心思路

Skill 本身是被动的——需要有人或有机制来"唤醒"它。自动 tick 的本质就是**用 OS 级调度工具或 scheduler 定期执行执行器的非交互命令**，例如：

1. `claude -p "/agent command" --print`
2. `opencode run -m <model> "/agent command"`

## 已验证可用的方案

### 方案一：cron + 非交互命令（macOS/Linux，最可靠）

```bash
# 编辑 crontab
crontab -e

# Claude：每天早上 9:00 自动执行 go 命令
0 9 * * * cd /path/to/project && claude -p "/evo-skill-creator go" --allowedTools "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch" --print >> /tmp/evo-skill-tick.log 2>&1

# Claude：每周一早上 8:00 自动 scan
0 8 * * 1 cd /path/to/project && claude -p "/evo-skill-creator scan" --print >> /tmp/evo-skill-scan.log 2>&1

# OpenCode：每周五下午 5:00 自动 review
0 17 * * 5 cd /path/to/project && opencode run -m opencode/mimo-v2-pro-free "/evo-skill-creator review" >> /tmp/evo-skill-review.log 2>&1

# OpenCode：每天整点自动 learn
0 * * * * cd /path/to/project && opencode run -m opencode/nemotron-3-super-free "/evo-skill-creator learn" >> /tmp/evo-skill-learn.log 2>&1

# Claude：每周五下午 5:00 自动 review
0 17 * * 5 cd /path/to/project && claude -p "/evo-skill-creator review" --print >> /tmp/evo-skill-review.log 2>&1
```

**优点**：持久、可靠、OS 重启后自动恢复
**注意**：需要 `--allowedTools` 或 `--dangerously-skip-permissions` 授权工具使用

### 方案二：launchd plist（macOS 原生，比 cron 更推荐）

创建 `~/Library/LaunchAgents/com.evo-skill-creator.tick.plist`，实现登录后自动启动定期任务。

### 方案三：Shell 脚本 + 手动/半自动触发

```bash
#!/bin/bash
# tick.sh — 一键执行所有定期任务
cd /path/to/project
echo "[$(date)] === tick start ===" >> tick.log
claude -p "/evo-skill-creator go" --print >> tick.log 2>&1
echo "[$(date)] === tick end ===" >> tick.log
```

老板可以随时 `./tick.sh` 或把它加入任何调度系统。

### 方案四：其他调度框架

- **systemd timer**（Linux）
- **Windows Task Scheduler**
- **PM2 / supervisord** — 进程管理器，可以配置定期重启
- **GitHub Actions** — 如果项目在 GitHub 上，可以用 Actions cron 触发

## 关键参数

| 参数 | 作用 | 说明 |
|------|------|------|
| `-p` / `--print` | Claude 非交互模式 | 执行完直接退出，适合自动化 |
| `run` | OpenCode 非交互模式 | 直接执行消息并退出 |
| `-m` | OpenCode 运行时选模型 | 适合按命令切换免费模型 |
| `--allowedTools` | Claude 指定允许的工具 | 自动模式下需要预授权 |
| `--dangerously-skip-permissions` | Claude 跳过权限检查 | 仅在安全环境使用 |
| `--max-budget-usd` | Claude 预算上限 | 防止失控消费 |
| `-c` / `--continue` | 继续上次会话 | 保持上下文连续性 |

## 推荐的 tick 策略

| 命令 | 频率 | 说明 |
|------|------|------|
| go | 每天 | 检查 backlog，做最紧急的事 |
| scan | 每周 | 扫描新趋势 |
| review | 每周 | 自省 |
| plan | 每月 | 更新学习计划 |
| learn | 按需 | 有新学习项时触发 |
| suggest | 不自动 | 需要老板输入，不适合自动 |
| status | 不自动 | 按需查看 |

## Hooks（事件驱动，已验证）

Claude Code 的 Hooks 机制是真实可用的，配置在 `.claude/settings.json`：

| Hook 类型 | 触发时机 | 可能的用途 |
|----------|---------|-----------|
| PreToolUse | 工具调用前 | 权限检查 |
| PostToolUse | 工具调用后 | 自动格式化 |
| Notification | 需要输入时 | 桌面通知 |
| Stop | 会话结束时 | 自动写日志 |

## 需要老板确认的事项

1. 是否要配置 cron 自动 tick？
2. tick 频率偏好（每天/每周？）
3. 是否愿意用 `--dangerously-skip-permissions` 或指定 `--allowedTools`？
4. API 预算上限设多少？

## 新启示

如果不同命令对执行器、模型、工具权限要求差异明显，单纯依靠 OS 级 cron 命令会越来越难维护。

更理想的方式是：

1. 用统一的 `evo-skills-scheduler`
2. 在配置文件中允许按命令覆盖 `executor`
3. 按命令覆盖 `model`
4. 按命令覆盖 `tools`

这样 `go`、`learn`、`plan`、`review` 可以天然走不同模型，而不是整角色绑定同一个默认值。
