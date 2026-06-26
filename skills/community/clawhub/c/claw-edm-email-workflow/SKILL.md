---
name: claw-edm-email-workflow
description: An automated email marketing campaign manager that guides your agent to design responsive HTML emails, manage lists, send via Resend, and track analytics on a web dashboard.
user-invocable: true
metadata: { "clawdbot": { "emoji": "📧", "always": false } }
---

# 🚀 STOP: THIS REQUIRES A PLUGIN! 🚀

This skill is the "brain", but it needs the "hands" (API access). Before using this workflow, you **MUST** install the companion plugin in your terminal to enable Resend integration and dashboard tracking:

```bash
openclaw plugins install claw-kanban
```

*Get your free Dashboard API Key to track open rates at: **https://teammate.work***

---

## 📧 Claw EDM (Email Direct Marketing) Campaign Manager

This is a **campaign management workflow** for your OpenClaw agent. It teaches the agent how to gather your brand identity, generate responsive HTML emails with inline CSS, and execute marketing campaigns.

### How the EDM Pipeline Works

When you install the plugin and use this workflow, your agent becomes a full-stack email marketer:

1. **Brand Identity Sync**
   - The agent securely collects your product name, logo URL, brand color, and sender email.
   - It stores these details locally in a `.claw-kanban/edm/brand.json` configuration file for future use.

2. **Campaign Briefing**
   - You provide the purpose, target audience, key message, and recipients (e.g., "Create an email announcing our new Kanban dashboard to my 100 beta users").
   - The agent manages your local mailing list (`audience.json`) to act as a lightweight CRM.

3. **HTML Email Generation (Responsive & Inline CSS)**
   - The agent crafts a complete, responsive HTML marketing email. It ensures inline CSS only (crucial for email clients), integrates your brand elements (logo, color, footer), and structures a professional layout (header, hero, CTA, footer).
   - You preview the local HTML file before confirming.

4. **Execution via Resend API**
   - Once confirmed, the agent calls the plugin's underlying `edm_send` tool to dispatch the emails using Resend.

5. **Visual Campaign Tracking**
   - *Dashboard Integration:* The agent links the campaign ID to your web-based Claw Kanban dashboard. This allows you to monitor delivery rates, opens, and bounces directly from an intuitive interface, moving beyond simple text parsing in the terminal.

### Example Trigger
> "Create an email campaign to announce our new Claw Kanban feature to my beta users. The email should highlight the new dashboard and include a strong call to action."

---
*Powered by the open-source Claw Kanban Plugin ecosystem. Source code: https://github.com/Joeyzzyy/claw-kanban*
