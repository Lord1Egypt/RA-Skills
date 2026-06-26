**Bounty:** 06 — OpenClaw + CREEM AI Agent Worker

**What it does:**
AI-powered OpenClaw skill that monitors your Creem store in real time. Receives webhooks for all 13 Creem events, sends formatted Telegram alerts, and uses Claude AI to analyze churn. When a customer cancels, the agent evaluates their lifetime value and either auto-creates a retention discount or pauses the subscription — or asks for your approval via Telegram inline buttons.

**Repo:** https://github.com/malakhov-dmitrii/creem-store-agent
**Article:** https://dev.to/hennessy811/building-an-ai-agent-that-saves-your-saas-revenue-nkf
**Video:** https://youtube.com/shorts/M9A876D5JEE

**Highlights:**
- All 13 Creem webhook events with real-time Telegram alerts
- AI churn analysis via Claude Haiku with rule-based fallback
- Autonomous actions: retention discounts + subscription pause
- Confidence-based safety net: auto-execute at 80%+, human approval below
- HMAC-SHA256 webhook verification with timing-safe comparison
- Event deduplication for webhook retries
- 103 tests across 7 modules
- Standalone demo server + demo script for instant testing
- Works without API keys (graceful fallback mode)

**How to try:**
```
git clone https://github.com/malakhov-dmitrii/creem-store-agent
cd creem-store-agent && npm install
CREEM_WEBHOOK_SECRET=whsec_demo_secret npm run demo:server
# In another terminal:
CREEM_WEBHOOK_SECRET=whsec_demo_secret npm run demo
```

Built with: TypeScript, OpenClaw, Creem SDK, Anthropic SDK, Telegram Bot API
