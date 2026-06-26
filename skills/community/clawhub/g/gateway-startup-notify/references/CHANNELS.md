# Channel Reference

All channels use `openclaw message send` via `execFile` with array arguments (no shell injection).

## Telegram

- **Address:** `@username` or numeric chat ID
- **Requires:** Telegram bot configured in OpenClaw

## WhatsApp

- **Address:** E.164 format (`+countrycodenumber`)
- **Requires:** WhatsApp configured in OpenClaw

## Discord

- **Address:** Numeric channel ID
- **Requires:** Discord bot configured in OpenClaw

## Slack

- **Address:** `#channel-name` or channel ID (e.g. `C1234567890`)
- **Requires:** Slack workspace connected in OpenClaw

## Signal

- **Address:** E.164 format (`+countrycodenumber`)
- **Requires:** Signal configured in OpenClaw

## iMessage

- **Address:** Apple ID email or phone number
- **Requires:** iMessage configured in OpenClaw

## Google Chat

- **Address:** Space ID (e.g. `spaces/AAAAAAAAAAA`)
- **Requires:** Google Chat configured in OpenClaw

## IRC

- **Address:** `#channel-name`
- **Requires:** IRC configured in OpenClaw

## Line

- **Address:** Line user ID
- **Requires:** Line configured in OpenClaw

## WeChat (openclaw-weixin)

- **Address:** User openid in `openid@im.wechat` format
- **Requires:** openclaw-weixin plugin configured via `openclaw channels`
- **Setup:** `openclaw channels add --channel openclaw-weixin --token "<token>"`

## Feishu / Lark

- **Address:** Chat ID (e.g. `oc_xxx`) or user ID
- **Requires:** Feishu/Lark plugin configured via `openclaw channels`
- **Setup:** See OpenClaw docs for feishu channel configuration
- **Note:** Bundled plugin — connect via WebSocket, no public webhook needed

## QQ Bot

- **Address:** Numeric chat ID
- **Requires:** QQ Bot plugin configured via `openclaw channels`
- **Setup:** `openclaw channels add --channel qqbot --token "AppID:AppSecret"`
- **Note:** Supports C2C private chat, group @messages, and guild channel messages
