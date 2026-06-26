# OpenClaw Query Examples

Use this file when you know the user intent but need a high-signal `rg` query quickly.

## Install and Setup

- User asks: "How do I install OpenClaw on Raspberry Pi?"
  - `rg --files openclaw_docs/platforms openclaw_docs/install openclaw_docs/start | rg 'raspberry-pi|quickstart|install'`
- User asks: "How do I upgrade OpenClaw safely?"
  - `rg -n "upgrade|update|migrat|version" openclaw_docs/install openclaw_docs/start`
- User asks: "How do I uninstall OpenClaw?"
  - `rg --files openclaw_docs | rg 'uninstall'`

## Gateway and Runtime

- User asks: "How does gateway authentication work?"
  - `rg -n "auth|authentication|token|scope|pair" openclaw_docs/gateway`
- User asks: "What is sandbox vs elevated execution?"
  - `rg -n "sandbox|elevated|approval|policy" openclaw_docs/gateway openclaw_docs/tools`
- User asks: "How does heartbeat/discovery work?"
  - `rg -n "heartbeat|discovery|bonjour" openclaw_docs/gateway`

## CLI

- User asks: "How to use `openclaw models`?"
  - `rg -n "models" openclaw_docs/cli openclaw_docs/providers`
- User asks: "How do approvals work from CLI?"
  - `rg -n "approval|approve|exec" openclaw_docs/cli openclaw_docs/tools`
- User asks: "How to inspect health/status?"
  - `rg -n "health|status|doctor|diagnostic" openclaw_docs/cli openclaw_docs/help`

## Channels and Integrations

- User asks: "How to configure Telegram channel?"
  - `rg --files openclaw_docs/channels openclaw_docs/cli | rg 'telegram|pairing|channels'`
  - `rg -n "telegram|bot|token|webhook|pairing" openclaw_docs/channels/telegram.md openclaw_docs/cli/channels.md`
- User asks: "How to set up Slack/Discord?"
  - `rg -n "slack|discord|token|event|approval" openclaw_docs/channels`
- User asks: "How does group messaging or routing work?"
  - `rg -n "group|routing|broadcast|pairing" openclaw_docs/channels`

## Security and Troubleshooting

- User asks: "Where are security recommendations?"
  - `rg --files openclaw_docs | rg 'security|threat|auth'`
- User asks: "Why is exec blocked?"
  - `rg -n "blocked|deny|approval|sandbox|elevated" openclaw_docs/tools openclaw_docs/gateway openclaw_docs/help`
- User asks: "How to debug provider/model issues?"
  - `rg -n "provider|model|failover|retry|quota|error" openclaw_docs/providers openclaw_docs/concepts openclaw_docs/help`

## Query Tuning Rules

- Start broad with filenames, then narrow by subdirectory and keywords.
- Prefer 2-4 intent keywords over one generic word.
- Add platform/tool constraints (`macos`, `gateway`, `cli`) to reduce noise.
- After finding candidate files, read full files before answering defaults or behavior.
