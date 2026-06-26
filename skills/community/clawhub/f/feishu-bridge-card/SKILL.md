---
name: feishu-bridge
description: Bridging OpenClaw reports and alerts to Feishu (Lark) for VPN-free delivery in China. Use when: (1) Sending the 7:45 AM EST Portfolio Synergy report, (2) Sending the 8:00 AM AI Frontier Sentinel or Job Tracker report, (3) Pushing urgent global news alerts.
---

# Feishu Bridge

## 🛰️ Connectivity
- **Webhook URL**: `https://open.feishu.cn/open-apis/bot/v2/hook/abe2e939-a15a-44ba-b818-1cc01048b782`
- **Method**: POST JSON to the webhook endpoint.

## 📡 Usage
Use the bundled Python script to send reports:
`python3 scripts/send_msg.py "WEBHOOK_URL" "YOUR_CONTENT"`

## 📋 Reporting Protocol
1. **Generate Report**: Follow the styles defined in `portfolio-synergy`, `ai-frontier-sentinel`, or `global-news-sentinel`.
2. **Push to Feishu**: Use this bridge as the primary delivery channel for users in VPN-restricted regions.
3. **Format**: Ensure content is properly escaped for JSON.
