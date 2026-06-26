# ⚡ boot-resume

**Zero-cooperation session recovery after gateway restart or system wake.**

No checkpoints, no hooks, no agent involvement — just reads the evidence and picks up where it left off.

## Why

Your agent is halfway through a task. The gateway restarts. The agent goes silent. You have to manually tell it to continue — for _every_ interrupted session.

Checkpoint-based solutions require the agent to save state _before_ dying. But SIGKILL, OOM, and power loss don't give it that chance.

**boot-resume** takes a different approach: it reads the JSONL session files _after_ the restart to detect what was interrupted, then automatically injects a resume event. No pre-save. Works after SIGKILL.

## How It Works

A shell script runs on every gateway start (systemd `ExecStartPost`) and every system wake from sleep/suspend (`sleep.target`):

```
Scan sessions.json → Detect via JSONL tail → Resume via cron --system-event
```

| Last JSONL Entry | Meaning | Action |
|---|---|---|
| `toolResult` | Agent was mid-execution | Resume |
| `assistant` (empty text) | Tool call in flight | Resume |
| `user` (non-trivial) | Message never processed | Resume |
| `assistant` (with text) | Completed normally | Skip |

No LLM involved in detection. 100% deterministic.

## Install

```bash
bash ~/.openclaw/workspace/skills/boot-resume/install.sh
```

Or manually:

```bash
cp scripts/boot-resume-check.sh ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/boot-resume-check.sh
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cp templates/boot-resume.conf ~/.config/systemd/user/openclaw-gateway.service.d/
cp templates/boot-resume-wake.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable boot-resume-wake.service
```

## Test

1. Send your agent a task that takes time
2. Wait for it to start processing
3. `systemctl --user restart openclaw-gateway`
4. Agent resumes within ~35 seconds

## Features

- **Dual trigger** — gateway restart (ExecStartPost) + system sleep/wake (sleep.target)
- Multi-agent support (scans all agents, not just `main`)
- Smart session filtering (skips cron, subagent, heartbeat sessions)
- Log rotation, error visibility, deduplication
- `--no-wait` flag for manual invocation via `/boot-resume`

## Configuration

Edit `scripts/boot-resume-check.sh`:
- `WINDOW_MINUTES=20` — scan window
- `DELAY=20s` — delay before resume injection

## Comparison

| Feature | boot-resume | Checkpoint-based |
|---|---|---|
| Pre-save required | No | Yes |
| Survives SIGKILL/OOM | Yes | No |
| LLM-free detection | Yes | No |
| Agent cooperation | None | Must write checkpoints |

## License

MIT

---

# ⚡ boot-resume（中文）

**网关重启或系统唤醒后自动恢复中断的会话。无需 agent 配合。**

不需要 checkpoint 文件，不需要预存钩子，不需要 agent 做任何事 —— 只读取已有的证据，自动接上中断的任务。

## 为什么需要

你的 agent 正在执行一个多步任务，网关突然重启了。Agent 不再响应，你必须手动对每个中断的会话说"继续"。

现有方案（checkpoint、快照文件）要求 agent 在崩溃前保存状态。但 SIGKILL、OOM、断电根本不给 agent 保存的机会。

**boot-resume** 换了一个思路：重启后直接读 JSONL 会话文件，检测哪些会话被中断了，然后自动注入恢复事件。不需要预存任何东西。SIGKILL 后也能恢复。

## 工作原理

一个 shell 脚本在每次网关启动（systemd `ExecStartPost`）和系统从休眠唤醒（`sleep.target`）时自动运行：

```
扫描 sessions.json → 读 JSONL 尾部检测中断 → 通过 cron --system-event 注入恢复
```

| JSONL 最后一条 | 含义 | 动作 |
|---|---|---|
| `toolResult` | agent 正在执行中 | 恢复 |
| `assistant`（空文本）| tool call 已发出 | 恢复 |
| `user`（非trivial）| 消息未处理 | 恢复 |
| `assistant`（有文本）| 正常结束 | 跳过 |

检测过程不涉及 LLM。100% 确定性。

## 安装

```bash
bash ~/.openclaw/workspace/skills/boot-resume/install.sh
```

## 测试

1. 给 agent 发一个需要时间的任务
2. 等它开始处理（tool call 进行中）
3. `systemctl --user restart openclaw-gateway`
4. agent 约 35 秒内自动恢复

## 特性

- **双重触发** — 网关重启（ExecStartPost）+ 系统休眠唤醒（sleep.target）
- 多 agent 支持（扫描所有 agent，不只是 main）
- 智能会话过滤（跳过 cron、子agent、heartbeat 会话）
- 日志轮转、错误可见、去重
- 手动调用：`/boot-resume`（通过 `--no-wait` 跳过启动延迟）

## 配置

编辑 `scripts/boot-resume-check.sh` 顶部变量：
- `WINDOW_MINUTES=20` — 扫描时间窗口
- `DELAY=20s` — 恢复注入延迟

## 对比

| 特性 | boot-resume | checkpoint 方案 |
|---|---|---|
| 需要预存 | 否 | 是 |
| SIGKILL/OOM 后可恢复 | 是 | 否 |
| 检测无需 LLM | 是 | 否 |
| 需要 agent 配合 | 不需要 | 必须写 checkpoint |

## 许可证

MIT
