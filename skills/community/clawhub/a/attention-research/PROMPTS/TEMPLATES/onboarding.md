# Onboarding Prompt — Attention Research

*Version 2.0.0 | First interaction when user wants to add a new topic*

---

## Step 1: Ask Only the Topic

When a user says:
- "I want to track biotech"
- "Add climate research"
- "Monitor the US-China tech war"

Respond with entity weights, signal criteria, noise filters, and cadence for the topic.

---

## Requirements Check (Before Activation)

Before activating any topic, verify:

| Requirement | How to check | If missing |
|-------------|--------------|------------|
| **Web search tool** | Agent has a working web_search capability | Configure the agent's search provider |
| **OpenClaw cron daemon** | `openclaw cron status` shows jobs | Start with `openclaw gateway start` |
| **Delivery channel** | Telegram chat_id or WhatsApp configured | Ask user for Telegram chat ID |
| **Research root** | `~/.openclaw/workspace/docs/research/` exists | Run `SCRIPTS/setup-cron.sh` |

If a requirement is missing:
```
Can't activate [topic] yet. Missing:
- [requirement]: [how to fix]
Fix it and I'll add the topic. Live on next cron run once ready.
```

---

## Pre-Built Topic Defaults

### us-iran-conflict
Entities: US govt 30%, Iran leadership 30%, Gulf states 12%, Israel 8%, EU 8%, Pakistan 6%, UN 4%, Shipping 2%
Cadence: Both morning + afternoon

### ai
Entities: Frontier labs 25%, Infra providers 20%, Hyperscalers 20%, US govt 15%, China/Huawei 10%, EU 5%, Academic 5%
Cadence: Both morning + afternoon

### geopolitics
Entities: Major powers 40%, Regional powers 25%, Multilateral 15%, Trade blocs 10%, Non-state 5%, Swing 5%
Cadence: Both morning + afternoon

### finance-markets
Entities: Central banks 25%, Institutional investors 20%, Governments 15%, Rating agencies 8%, IMF/World Bank 7%, Corporate 15%, Retail 5%
Cadence: Both morning + afternoon

### climate-changes
Entities: Governments 30%, Energy sector 25%, Science institutions 15%, Regulators 10%, Financial institutions 10%, NGOs 5%, Agriculture 5%
Cadence: Morning only

### bio-tech
Entities: FDA 25%, Large pharma 20%, Clinical biotech 20%, Institutional investors 15%, KOLs 10%, Academic 10%
Cadence: Both morning + afternoon

---

## After Proposing Defaults

```
To activate this topic:

Approve as-is  →  I verify requirements, add to CONFIG/topics.yaml, live next cron run.
Adjust          →  Tell me what to change (entities, signals, cadence, noise filters).
Customize       →  Drop in a paper/thesis and I'll rebuild the framework from it.

Topic name: [user's topic]
Status: pending your input
```

---

*Version 2.0.0 | 2026-04-20*