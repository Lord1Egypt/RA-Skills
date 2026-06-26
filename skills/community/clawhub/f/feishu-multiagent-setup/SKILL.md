---
name: feishu-multiagent-setup
description: "飞书多机器人接入 OpenClaw 的配置向导。用于给用户生成步骤清单、字段说明、权限核对表和本地配置草案；公开版不收集真实 App Secret/API Key，不写入 openclaw.json，不运行脚本，不重启服务。需要处理密钥或改配置时，必须让用户在本机私有环境中确认和执行。"
version: 1.0.2
---

# Feishu Multiagent Setup

Use this skill when a user wants to connect multiple Feishu bots to OpenClaw and needs a safe setup checklist.

## Public Safety Boundary

- Do not ask the user to paste real App Secret, API Key, Verification Token, Encrypt Key, cookies, or login state into chat.
- Do not write `openclaw.json`, `auth-profiles.json`, shell profiles, service files, or gateway config from this public skill.
- Do not run setup scripts or restart Gateway from this public skill.
- Do not bypass Feishu login, QR code, captcha, organization approval, or admin authorization.
- If the user wants private execution, first explain what will be written and ask for explicit confirmation in their local environment.

## Workflow

1. Ask how many bots they need and what each bot should be used for.
2. Generate a table with safe placeholders:
   - bot name
   - Feishu app display name
   - event subscription URL placeholder
   - required permissions/events
   - local config destination
3. Guide the user through Feishu Open Platform pages by visible Chinese labels.
4. When credentials appear, tell the user to keep them in a local private config file, not in public docs or chat history.
5. Produce a local review checklist for their OpenClaw operator:
   - each bot has one account id
   - each account id has one route binding
   - each route binding points to the intended agent
   - each agent has an isolated workspace
   - test messages are sent only after the user confirms setup is complete

## Output Shape

Return a concise checklist plus a local-only config draft with placeholders. Example:

```text
bot_name: customer_service_bot
feishu_app_id: cli_xxx_placeholder
secret_storage: local private config only
route: feishu:<account_id> -> agent:<agent_id>
status: pending user-side credential entry
```

## Reference

Read `references/setup-checklist.md` when the user needs a full step-by-step handoff.
