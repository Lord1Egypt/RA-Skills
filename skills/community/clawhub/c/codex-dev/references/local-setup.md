# Local setup | 本地配置

This package publishes a skill, not a full OpenClaw runtime state.

这个包发布的是 skill，不是你本机完整的 OpenClaw 运行状态。

It is best suited for local async development workflows where you want:

- an immediate job receipt
- saved logs and patch artifacts
- optional Telegram completion messages
- a user-selectable working directory

它特别适合这样的本地异步开发场景：

- 先拿到作业回执
- 保留日志和补丁产物
- 可选地把完成结果发到 Telegram
- 允许用户指定工作目录

## What you still configure locally | 仍需本地配置的内容

- your Telegram bot token
- your Telegram chat id
- your preferred default work directory
- your OpenClaw agent binding and routing

你仍然需要在本地自行配置：

- Telegram bot token
- Telegram chat id
- 默认工作目录
- OpenClaw agent 绑定和路由

## Suggested local environment | 建议的本地环境变量

```bash
export CODEX_DEV_DEFAULT_WORKDIR="/absolute/path/to/your/repo"
export CODEX_DEV_CHAT_ID="123456789"
export TELEGRAM_BOT_TOKEN="your-bot-token"
```

## Telegram 审批 | Telegram Exec Approvals

If you want to approve exec requests directly from Telegram, enable Telegram exec approvals in your local OpenClaw config.  
如果你希望直接在 Telegram 里审批执行请求，需要在本地 OpenClaw 配置中启用 Telegram 执行审批。

Recommended minimum settings:  
建议的最小配置：

```json
{
  "channels": {
    "telegram": {
      "execApprovals": {
        "enabled": true,
        "approvers": [8249736863],
        "agentFilter": ["main", "openclaw-dev-codex"],
        "target": "dm"
      }
    }
  }
}
```

Notes:  
说明：

- `approvers` should be the numeric Telegram user id that is allowed to approve.
- `approvers` 应填写允许审批的 Telegram 数字用户 ID。
- `target: "dm"` is the safest default because approval prompts stay in a private chat.
- `target: "dm"` 是最安全的默认值，因为审批提示会留在私聊里。
- If you need approvals to appear in the originating Telegram chat/topic, use `"channel"` or `"both"` only in trusted chats.
- 如果你需要让审批提示直接出现在当前 Telegram 聊天/话题里，只应在受信任聊天中使用 `"channel"` 或 `"both"`。
- After changing the config, restart the gateway.
- 改完配置后，需要重启 gateway。

Verification flow:  
验证流程：

```bash
systemctl --user restart openclaw-gateway.service
openclaw channels status
```

Approval stability note:  
审批稳定性说明：

- Do not restart `openclaw-gateway.service` while a Telegram exec approval prompt is still waiting for `/approve`.
- 当 Telegram exec 审批单还在等待 `/approve` 时，不要重启 `openclaw-gateway.service`。
- A gateway restart invalidates the current approval id, and Telegram will return `unknown or expired approval id`.
- gateway 重启会让当前审批 ID 失效，随后 Telegram 会返回 `unknown or expired approval id`。

If `/approve` still says it needs `operator.approvals`, the current Telegram client session is missing the approval scope and should be re-paired/upgraded through the Control UI or device pairing flow.  
如果 `/approve` 仍提示缺少 `operator.approvals`，说明当前 Telegram 客户端会话还没有审批 scope，需要通过 Control UI 或设备配对流程重新配对/升级权限。

## Optional wrapper install | 可选的包装命令安装

From the installed skill folder:
从已安装的 skill 目录执行：

```bash
./scripts/install-local.sh "$HOME/bin"
```

That creates:
它会创建：

- `codex-dev`
- `codex-help`
- `codex-dev-status`
- `codex-dev-show`
- `codex-dev-dispatch`

## Suggested OpenClaw agent binding | 建议的 OpenClaw agent 绑定

Create or update a dedicated Telegram-bound agent that knows:
创建或更新一个专用于 Telegram 的 agent，并确保它知道：

- write requests should use `codex-dev`
- read-only requests can answer directly
- `/codex-dev ...` is a forced async request
- `/codex-help` and `/codex-dev help` should return usage guidance
- when developing a reusable skill, never bake the current task's keywords, sites, or project names into default behavior
- task-specific presets belong in examples, references, or separate preset files, not in the generic skill default path
- write requests should default to `--workdir /home/fzhlian/Code/codex-dev` unless the user explicitly names another path

Recommended user-facing examples:

- `/codex-dev fix one bug and summarize the change`
- `/codex-dev --workdir /absolute/path fix the issue only here`
- `/codex-help`
- `/codex-dev 修一个 bug 并总结修改`
- `/codex-dev --workdir /absolute/path 只在这个目录里修复问题`
- `/codex-help`

## Suggested publish metadata | 建议的发布元数据

- slug: `codex-dev`
- version: start with `0.1.0`
- tags: `latest,codex,async,telegram`
