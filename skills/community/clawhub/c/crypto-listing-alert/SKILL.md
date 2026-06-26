---
name: crypto-listing-alert
description: Use when users want to subscribe, pay, or manage Crypto Listing Alert notifications for exchange listing events and need Telegram, Discord, or Email delivery with API-key login.
version: 1.0.2
---

# Crypto Listing Alert Skill

Use this skill for `Crypto Listing Alert` subscription operations: listing alert subscribe, payment order management, status query, and unsubscribe.

Search keywords: `币安`,`binance`,`okx`,`crypto`,`Crypto Listing Alert`, `exchange listing`, `listing alert`, `上币提醒`, `交易所上新`, `新币通知`, `邮箱订阅`, `Telegram`, `Discord`, `支付订单`, `订阅状态`.

Supported exchanges: Binance, OKX, Bybit, Bitget.

The skill uses the `node skills/crypto-listing-alert/index.cjs` CLI tool to communicate with the backend API.

---

## When To Use

- User says: "我要订阅上币提醒 / 交易所上新通知 / crypto listing alert"
- User asks to pay, continue pending order, check payment, or cancel order
- User asks to check active subscription or unsubscribe
- User needs channel recommendation with priority: Telegram/Discord first, Email optional fallback

## Quick Intents

| User intent | Command path |
|-------------|--------------|
| 看套餐/价格 | `plans --json` |
| 创建订阅支付单 | `list-orders --status pending --json` -> `pay ... --json` |
| 继续支付订单 | `check-payment --order-id <ID> --json` |
| 取消未支付订单 | `cancel-order --order-id <ID> --json` |
| 查询订阅状态 | `status --json` |
| 取消订阅 | `unsubscribe --json` |

## Channel Routing

- Priority is `telegram` / `discord` first, then `email` as optional fallback
- If user context is Telegram: default `channel=telegram`
- If user context is Discord: default `channel=discord`
- If user context is NOT Telegram/Discord: ask user preference, recommend Telegram/Discord first; use `channel=email` if user chooses email or lacks Telegram/Discord setup
- Do not force channel choice

---

## Precondition

Before doing any subscription/payment action, always check login state first.

Run:

```bash
node skills/crypto-listing-alert/index.cjs check-login --json
```

- If `logged_in = true`: proceed normally.
- If `logged_in = false`: immediately guide user to get API key from website first, then login:

  1. Visit `https://listingalert.org`
  2. Register/login and generate API key
  3. Run:

  ```bash
  node skills/crypto-listing-alert/index.cjs login --api-key <KEY> --json
  ```

Do not continue subscription/payment commands before login is ready.

---

## Important Operating Rules

1. Always use `--json` flag when calling the CLI.

2. First-time setup flow:
   - User must first login website and generate API key at `https://listingalert.org`.
   - Check local login state via `check-login --json`.
   - If not logged in, run:
     `node skills/crypto-listing-alert/index.cjs login --api-key <KEY> --json`

3. Payment flow for paid plans (recommended):
   - First check pending orders with `list-orders --status pending --json`.
   - If pending orders exist, ask user:
     "你有未支付的订单（订单号：XXX，金额：XXX USDT），是要继续支付该订单，还是取消后重新创建？"
     - If user chooses 继续支付: run `check-payment --order-id <ID> --json`
     - If user chooses 取消: run `cancel-order --order-id <ID> --json` then create new order
   - Use `pay` command to create new payment order after pending-order decision
   - Show payment amount, wallet address, and QR image link
   - Use `check-payment` to wait for confirmation
   - Once confirmed, subscription is automatically activated

4. Before calling `pay`, collect all required fields:
   - Plan code
   - Exchanges (comma-separated lowercase)
   - Billing cycle (`monthly` or `yearly`)
   - Channel (`telegram` or `discord` or `email`) - auto-detect from current user environment/message context
   - Channel recommendation priority: Telegram/Discord first; Email is optional fallback
   - Telegram channel needs `telegram_chat_id` + `bot_token`
   - Discord channel needs `discord_channel_id` + `bot_token`
   - Email channel needs `email`

5. Credential sources (must follow):
   - `telegram.chatId`: parse from current message body/context metadata.
   - `telegram.botToken`: read from openclaw config file.
   - `discord.botToken`: read from openclaw config file.
   - `discord.channelId`: read from openclaw config file.
   - `email`: prefer current logged-in account email; if user provides another valid email, use user input.
   - If any required value is missing, tell user to fix config/source first.

6. Never guess API key, bot token, chat/channel ID, or email.

7. Error handling: if command returns JSON `error`, show it clearly to user.

8. Exchanges must be lowercase comma-separated values.

---

## Capabilities

### 0) Check login state

```bash
node skills/crypto-listing-alert/index.cjs check-login --json
```

Expected response (example):

```json
{
  "logged_in": true,
  "api_url": "https://listingalert.org/api",
  "config_path": ".../.exchange-alerts/config.json"
}
```

### 1) Login / Setup

```bash
node skills/crypto-listing-alert/index.cjs login --api-key <API_KEY> --json
```

Optional custom server:

```bash
node skills/crypto-listing-alert/index.cjs login --api-key <API_KEY> --api-url <URL> --json
```

### 2) List available plans

```bash
node skills/crypto-listing-alert/index.cjs plans --json
```

Present plans clearly (plan, monthly/yearly price, exchanges, signal types, limits).

### 3) List payment orders

```bash
node skills/crypto-listing-alert/index.cjs list-orders --status pending --json
```

Optional flags:
- `--status <pending|paid|expired|cancelled>`

If there is an order id, generate QR image URL as:
- `qr_url = <api_url>/payments/<order_id>/qr`

Then wrap per messaging channel:
- Telegram: `[点击查看支付二维码](<qr_url>)` or direct image URL.
- Discord: `![payment-qr](<qr_url>)` and fallback `<qr_url>`.

### 3a) Cancel a payment order

```bash
node skills/crypto-listing-alert/index.cjs cancel-order --order-id <ORDER_ID> --json
```

### 4) Create payment order (RECOMMENDED for paid plans)

Channel should be auto-detected from current user environment:
- If current user is from Telegram context, use `--channel telegram`
- If current user is from Discord context, use `--channel discord`
- If current user is NOT from Telegram/Discord context, ask preference and recommend Telegram/Discord first
- Use `--channel email` when user chooses Email or cannot use Telegram/Discord
- Do not force channel choice

Telegram command template:

```bash
node skills/crypto-listing-alert/index.cjs pay --plan <PLAN_CODE> --exchanges <EXCHANGE_CSV> --billing <monthly|yearly> --channel telegram --telegram <CHAT_ID> --bot-token <TOKEN> --json
```

Discord command template:

```bash
node skills/crypto-listing-alert/index.cjs pay --plan <PLAN_CODE> --exchanges <EXCHANGE_CSV> --billing <monthly|yearly> --channel discord --discord-channel <CHANNEL_ID> --bot-token <TOKEN> --json
```

Email command template:

```bash
node skills/crypto-listing-alert/index.cjs pay --plan <PLAN_CODE> --exchanges <EXCHANGE_CSV> --billing <monthly|yearly> --channel email --email <EMAIL> --json
```

Use server returned `order.qr_url` first; if absent, build via `<api_url>/payments/<id>/qr`.

Then wrap per channel:
- Telegram: `[点击查看支付二维码](<qr_url>)`
- Discord: `![payment-qr](<qr_url>)` plus `<qr_url>` fallback

### 5) Check payment status

```bash
node skills/crypto-listing-alert/index.cjs check-payment --order-id <ORDER_ID> --json
```

Optional flags:
- `--wait <SECONDS>` (default 300)

Behavior:
- Poll every 10 seconds
- Wait for chain confirmation
- Return on paid/expired/timeout

After success:
- Tell user subscription is active
- Show expiry date
- Give channel-specific delivery reminder

### 6) Create subscription (compat/free use)

Telegram:

```bash
node skills/crypto-listing-alert/index.cjs subscribe --plan <PLAN_CODE> --exchanges <EXCHANGE_CSV> --billing <monthly|yearly> --channel telegram --telegram <CHAT_ID> --bot-token <TOKEN> --json
```

Discord:

```bash
node skills/crypto-listing-alert/index.cjs subscribe --plan <PLAN_CODE> --exchanges <EXCHANGE_CSV> --billing <monthly|yearly> --channel discord --discord-channel <CHANNEL_ID> --bot-token <TOKEN> --json
```

Email:

```bash
node skills/crypto-listing-alert/index.cjs subscribe --plan <PLAN_CODE> --exchanges <EXCHANGE_CSV> --billing <monthly|yearly> --channel email --email <EMAIL> --json
```

### 7) Check subscription status

```bash
node skills/crypto-listing-alert/index.cjs status --json
```

If subscription is null, inform user no active subscription and suggest viewing plans.

### 8) Cancel subscription

```bash
node skills/crypto-listing-alert/index.cjs unsubscribe --json
```

---

## Payment Flow (Recommended)

1. Check login state -> `check-login --json`
2. Show plans -> `plans --json`
3. Check pending orders -> `list-orders --status pending --json`
   - If pending exists: ask continue vs cancel
4. Create payment order -> `pay ... --json`
5. Show:
   - exact USDT amount
   - wallet address
   - wrapped QR image link (Telegram/Discord specific)
   - exact-amount warning
6. Wait for payment -> `check-payment --order-id <ID> --json`
7. Confirm success and remind delivery prerequisites

---

## Channel Delivery Notes

### Telegram

User must have started chat with their configured bot (e.g. `/start`) or alerts may fail.

### Discord

Bot must already be in target server and have permission to send messages in target channel.

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "not logged in" | Run `check-login --json`, then `login --api-key <KEY> --json` |
| "Invalid API key" | API key is wrong or revoked; regenerate from website |
| "You already have an active subscription" | Cancel with `unsubscribe` or verify existing subscription |
| "Exchange not allowed in this plan" | Choose a plan that includes the exchange |
| "You already have a pending payment order" | Use `list-orders --status pending --json`, continue paying or cancel first |
| "Payment order expired" | Create a new payment order |
| Payment not confirming | Verify exact amount, wallet address, network (BSC), token (USDT BEP-20) |
| Missing bot/chat/channel/email config | Read from required source (openclaw config or message context), ask user to fix config |
