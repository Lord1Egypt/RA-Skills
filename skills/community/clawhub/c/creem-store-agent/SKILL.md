---
name: creem-store-agent
description: "AI-powered Creem store monitor — alerts, churn analysis, autonomous actions via Telegram"
user-invocable: true
metadata:
  openclaw:
    emoji: "🍦"
    primaryEnv: CREEM_API_KEY
    requires:
      bins:
        - node
      env:
        - CREEM_API_KEY
        - CREEM_WEBHOOK_SECRET
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHAT_ID
        - ANTHROPIC_API_KEY
---

# Creem Store Agent

AI-powered monitoring for your Creem store. Sends real-time Telegram alerts for sales, subscriptions, disputes, and refunds. Uses Claude AI to analyze churn events and autonomously recommend retention actions.

## Commands

- `/creem-status` — Check store connection and webhook status
- `/creem-report` — Daily revenue summary (MRR, churn, new sales)

## Features

- **Real-time alerts**: Formatted Telegram notifications for all Creem events
- **AI churn analysis**: Claude Haiku analyzes cancellations and recommends retention actions
- **Autonomous actions**: Create retention discounts or pause subscriptions via inline buttons
- **Event deduplication**: Handles Creem webhook retries gracefully
- **HMAC verification**: Validates webhook signatures for security

## Setup

1. Install: `clawhub install creem-store-agent`
2. Set environment variables (see `.env.example`)
3. Expose webhook URL: `ngrok http 3000` (development)
4. Register webhook in Creem dashboard: `https://your-ngrok-url.ngrok.io/webhook/creem`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `CREEM_API_KEY` | Creem API key (test: `creem_test_xxx`) |
| `CREEM_WEBHOOK_SECRET` | Webhook signing secret from Creem dashboard |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude Haiku |
