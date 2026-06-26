---
name: bellink
description: Connect your AI to 30+ business tools — Gmail, Calendar, Sheets, Mindbody, Meta Ads, Linear, Airtable, Notion, Stripe, and more. One URL, every app.
version: 1.0.2
metadata:
  openclaw:
    requires:
      env:
        - BELLINK_URL
    primaryEnv: BELLINK_URL
    emoji: "🔗"
    homepage: https://www.bellink.io
---

# Bellink — AI Gateway to Business Tools

Connect your AI assistant to 30+ business tools through one MCP server.

## Setup (30 seconds)

1. Sign up at https://app.bellink.io (free Starter plan, no credit card)
2. Connect your apps (Gmail, Mindbody, Meta, etc.)
3. Copy your Bellink URL from the dashboard
4. Tell your bot: "add MCP server bellink: [paste URL]"

That's it. Your AI now has access to all your connected apps.

## Environment variable

The only credential needed is `BELLINK_URL` — the full MCP endpoint URL you copy from your Bellink dashboard. It contains your authentication key as a query parameter. No separate API key or Bearer token needed.

Example: `BELLINK_URL=https://app.bellink.io/api/mcp/server?key=your_key_here`

## What you can do

Once connected, just ask:

- "What's on my schedule today?" → pulls from Calendar + Mindbody
- "Send a reply to that email from John" → reads and sends via Gmail
- "What's my revenue this month?" → pulls from Mindbody or Stripe
- "Book Sarah for tomorrow's 9am class" → books directly in Mindbody
- "Create a spreadsheet with this month's sales" → writes to Google Sheets
- "Show me my Meta ad performance" → pulls campaign insights
- "Create a Linear issue for this bug" → creates in your project

## Supported apps

Gmail, Google Calendar, Google Sheets, Google Docs, Google Drive, Google Analytics, Google Forms, Mindbody, Meta (Facebook + Instagram + Ads), Linear, Airtable, Notion, Stripe, Slack, GitHub, Figma, Allegro, QuickBooks, Twilio, Webflow, WordPress, Typeform, Calendly, Beehiiv, Buttondown, n8n, Zoom, Shopify, WhatsApp, Outlook

## MCP config (alternative setup)

If you prefer manual config, add to your mcporter.json:

```json
{
  "mcpServers": {
    "bellink": {
      "baseUrl": "BELLINK_URL",
      "transport": "sse"
    }
  }
}
```

Replace `BELLINK_URL` with the URL from your Bellink dashboard (includes your key).

## npm package

Also available as an npm package for Claude Desktop, Cursor, and other stdio MCP clients:

```bash
BELLINK_URL=https://app.bellink.io/api/mcp/server?key=your_key npx bellink-mcp
```

## Security

- OAuth 2.0 for all app connections — Bellink never sees your passwords
- AES-256 encryption for stored credentials
- Your data stays in your apps — Bellink reads and acts, doesn't store
- Disconnect any app anytime with one click
- `BELLINK_URL` is the only credential — a scoped key that only accesses your connected apps

## Pricing

- Starter: Free forever — all apps (except Mindbody), 250 requests/month
- Personal: $29/mo — all apps including Mindbody, 1,000 requests/month
- Business: $99/mo — all apps, 10K requests/month, 5 seats

## Links

- Website: https://www.bellink.io
- Dashboard: https://app.bellink.io
- npm: https://www.npmjs.com/package/bellink-mcp
