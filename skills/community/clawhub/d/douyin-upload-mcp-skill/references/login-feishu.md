# Login And Feishu Flow

Use this reference for Feishu-triggered workflows, QR login, SMS verification, customer prompts, and watcher behavior.

## Feishu Triggers

Customer messages:

- `发布抖音`
- `发送二维码`
- `已登录`
- 6 位短信验证码
- `发布视频`
- `更新数据`
- `更新数据 30天`
- `数据报告`

OpenClaw gateway mode must pass source context into the single MCP entry:

```js
douyin__douyin_feishu_route_text({
  text: raw_user_message,
  messageId: feishu_message_id,
  chatId: feishu_conversation_label_or_chat_id
})
```

With `messageId/chatId`, all outbound QR images, SMS prompts, security screenshots, publish completion, data reports, and auto-reply summaries go back to the same Feishu DM or group that triggered the flow. Without source context, the skill falls back to `DOUYIN_FEISHU_RECEIVE_ID`.

If an agent forgets to pass `messageId/chatId`, the MCP server attempts a fallback lookup in recent OpenClaw Feishu session logs and chooses the newest message whose user text matches the routed text. This is a resilience fallback only; passing `chatId` explicitly is still preferred.

Watcher commands:

```bash
node scripts/feishu-reply-watcher.js poll --init
node scripts/feishu-reply-watcher.js watch --since-seconds 1800 --interval-ms 1000 --page-size 50 --max-pages 10
```

Complete Feishu loop:

- Customer sends `发布抖音`: check login. If logged in, reply `登录成功，请发送视频。`; if not logged in, send only QR-preparation prompt.
- Upstream agent sends fields with `视频地址` and `标题`: download assets, convert task, check login, continue the same publish chain.
- Customer sends `登录/重新登录/检查登录`: check login; do not send QR directly.
- Customer sends `发送二维码`: only then refresh/regenerate QR, quality-check it, and send the latest QR.
- Customer confirms scan with `已登录/已完成`: check page again. If Douyin requires SMS, click/request SMS and ask for 6 digits.
- Customer sends 6 digits: clear old code, fill latest code, click confirm/verify, then wait for page stabilization.

## Login Phases

- `phase=qrcode`: login expired. First remind customer to open Feishu on desktop and prepare Douyin App scan. Do not send stale QR paths.
- `phase=sms_verification`: only after QR scan if Douyin switches to SMS branch. Default is still QR-first.
- `phase=sms_code_input`: ask customer for 6-digit SMS code and submit it.
- `phase=logged_in`: continue publish/data/comment work.

Login success must wait 1-2 seconds after page transition. Only say `登录成功，请发送视频。` when creator backend signals are visible, such as creator home, content management, publish entry, or logged-in navigation.

## QR Rules

Send QR only after explicit `发送二维码` and customer readiness:

```bash
node scripts/douyin-login-monitor.js fresh-qr --send --customer-ready --max-qr-attempts 3
```

QR requirements:

- Refresh/regenerate before every capture.
- Wait until QR region finishes loading.
- Include safe margin around QR; do not crop just the visible `img`.
- Send only high-contrast, scannable QR.
- Do not send gray QR, refresh-overlay QR, expired QR, abnormal-size QR, or cropped QR.
- Saved QR images are under `$HOME/.openclaw/workspace/douyin-ops/temp/`.

After sending QR, say: `请立即用手机抖音 App 扫码。请在电脑端飞书查看二维码，不要在手机端保存图片后扫码。扫码确认后回复：已登录`

Do not continuously poll and spam the customer. Wait for `已登录/已完成`.

## SMS Rules

- Click `发送验证码/重新发送/获取验证码` before asking the customer for the SMS code.
- Do not ask for a code if the page never entered SMS flow.
- If a new code arrives, clear the old value first, fill the latest value, then click confirm/verify.
- If submission does not change page state, ask for a fresh code or manual handling.

Short customer prompt:

`抖音要求短信验证，请把 6 位短信验证码发给我，不要发送其他文字。`

## Security Verification

If Douyin shows slider, captcha, robot, device verification, or risk page:

- Do not bypass.
- Screenshot the page.
- Send shortest instruction to customer.

Prompt:

`抖音出现安全验证，当前无法自动处理。请按截图在当前浏览器完成验证，完成后回复“已完成”。`

## Customer Copy

QR expired/login expired:

`抖音需要重新登录。请在电脑端打开飞书，用手机抖音 App 准备扫码。准备好后回复：发送二维码`

Video confirmation:

`已收到视频。确认要发布到抖音请回复：发布视频`
