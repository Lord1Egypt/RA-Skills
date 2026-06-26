# freelancer-crm

**A CRM for freelancers that lives in WhatsApp. No HubSpot. No Salesforce. No subscriptions.**

You text your OpenClaw agent. It manages your clients.

```
clawhub install omermalix/freelancer-crm
```

---

## What it does

You run a freelance business. You have clients. Some go quiet. Some owe you money. Some need a proposal. You track all of this in your head, or in a spreadsheet, or you forget entirely.

This skill fixes that. Once installed, your OpenClaw agent becomes your personal CRM assistant — available on WhatsApp 24/7, no dashboard to log into, no software to learn.

**Tell your agent:**

> *"Add Sarah Ahmed as a new lead. She wants a mobile app for $1,500 in 3 weeks."*

> *"Who owes me money?"*

> *"Write a proposal for Ahmed for a React dashboard, $800, 2 weeks."*

> *"Check my follow-ups."*

Your agent does the work. You get a WhatsApp reply.

---

## The 5 things it does

**1. Follow-up detector**
Finds every client you have not contacted in more than 5 days (configurable). Drafts a personalised WhatsApp message. Asks you to approve before sending. You never lose a lead to silence again.

**2. Invoice tracker**
Watches your unpaid invoices. After 7 days with no payment (configurable), drafts a polite reminder. Shows you a live list of who owes what and for how long.

**3. Proposal generator**
You give it a name, project, price, and timeline. It generates a clean, professional proposal instantly. No templates to find, no documents to open.

**4. Client status board**
Ask *"show me all my clients"* and get a clear summary: active, overdue, silent, new lead. Your entire pipeline in one WhatsApp message.

**5. Monday morning digest**
Every Monday at 9am, your agent sends you a WhatsApp summary automatically: how many follow-ups needed, invoices overdue, proposals pending, and total outstanding revenue.

---

## WhatsApp — two options, you choose

This skill works with both methods. You pick during setup.

| | Option A — WhatsApp Bridge | Option B — Official API |
|---|---|---|
| **Cost** | Free | Free tier: 1,000 msg/mo |
| **Setup** | 5 min — scan QR code | 1–3 days — Meta verification |
| **Number** | Your existing number | Separate business number |
| **Best for** | Getting started immediately | Production, high volume |

Start with Option A. Upgrade to Option B when you need to.

---

## Installation

**Requirements:**
- OpenClaw running on Linux or VPS
- Python 3.10+
- Node.js 18+
- A GitHub account

**Install:**
```bash
clawhub install omermalix/freelancer-crm
```

**First-time setup:**
```bash
cd ~/.openclaw/skills/freelancer-crm
python3 setup.py
```

The setup wizard will ask you 4 questions in plain English, create your config, and send a test WhatsApp message to confirm everything works. Takes about 3 minutes.

---

## How your data is stored

Your client data lives in `clients.json` on your own machine. Nothing is sent to any external server. No cloud database. No third-party CRM. Your data stays yours.

`config.json` contains your WhatsApp credentials. It is excluded from version control via `.gitignore` and never leaves your server.

---

## Commands your agent understands

Once installed, talk to your agent naturally. It will figure out the right command. But for reference, the underlying CLI supports:

```bash
python3 crm_cli.py list
python3 crm_cli.py add <name> <status> <project> <amount> <phone>
python3 crm_cli.py update <id> <field> <value>
python3 crm_cli.py follow-ups
python3 crm_cli.py invoices
python3 crm_cli.py proposal <name> <project> <cost> <timeline>
python3 crm_cli.py digest
```

---

## Security

- All data stored locally on your machine — nothing sent to external servers
- `config.json` and `clients.json` excluded from version control
- No third-party data collection
- File locking on all write operations prevents data corruption
- VirusTotal scan badge visible on this skill's ClawHub page

This skill uses `exec`, `read`, `write`, and `web_fetch` permissions.
`exec` is used only to run the Python scripts included in this folder.
`web_fetch` is used only when sending WhatsApp messages via the official Meta API.
You can review every line of code before installing.

---

## Tested on

- Ubuntu 22.04 LTS (VPS)
- Ubuntu 24.04 LTS (VPS)
- Python 3.10, 3.11, 3.12
- OpenClaw with Llama 3, GPT-4o, Claude 3.5 Sonnet

---

## Want a done-for-you setup?

If you want this configured and running on your server without touching a terminal, I offer a paid setup service.

**What you get:**
- Full installation and configuration on your Linux VPS
- WhatsApp connection verified and tested
- Your first 3 clients added to the system
- 7 days of support if anything breaks

**Want a custom automation for your business?**
I build custom OpenClaw skills and automations for freelancers and small businesses.
- Email: umarmalik6685@gmail.com
- WhatsApp: +923336685600

**Price:** $149

## Changelog

**v1.0.2** — March 2026
- Added `add` and `update` commands to `crm_cli.py`
- Added `setup.py` onboarding wizard for non-developers
- Added filelock protection for concurrent write safety
- Added descriptive error messages to `send_message.py`
- Added phone number format validation
- Cleared personal test data from `clients.json`
- Added `.gitignore` to protect credentials

**v1.0.0** — March 2026
- Initial release

---

## Author

**omermalix** — Software developer building tools for freelancers.

Questions or issues? Open a GitHub issue or message me directly.
