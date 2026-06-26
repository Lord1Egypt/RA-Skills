# 🇧🇩 bKash / Nagad Transaction Tracker

> Track your daily spending across bKash, Nagad, Rocket,
> and cash — in Bengali or English — right from Telegram,
> WhatsApp, or Slack. Get an automatic weekly digest
> every Sunday morning.

---

## Quick Start

Once installed, just send a message:

```
bkash 450 lunch
sent 5000 to mum nagad
rickshaw 80 taka cash
electricity bill 1200 bkash
```

That's it. No forms. No apps. Just chat.

---

## Installation

```bash
clawhub install bkash-nagad-tracker
```

Then set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Requires Python 3.10+ installed on your system.

---

## Supported Languages

- ✅ English
- ✅ Bengali (বাংলা)
- ✅ Mixed Bengali + English

---

## Supported Payment Methods

| Method | Trigger words |
|--------|--------------|
| 🔴 bKash | bkash, bikash, বিকাশ |
| 🟠 Nagad | nagad, নগদ |
| 🟣 Rocket | rocket, রকেট |
| 💵 Cash | cash, নগদ টাকা |

---

## Example Messages

**English:**
```
bkash 450 lunch
sent 5000 to mum nagad
electricity bill 1200 bkash
rickshaw 80 cash
show my spending this week
```

**Bengali:**
```
বিকাশে ৪৫০ টাকা খাবার
মাকে ৫০০০ নগদে পাঠালাম
বিদ্যুৎ বিল ১২০০ বিকাশ
এই সপ্তাহে কত খরচ হলো
```

**Mixed:**
```
bkash dilam 1200 bill
rickshaw te 80 taka cash
lunch 350 bkash korলাম
```

---

## Commands

| Command | What it does |
|---------|-------------|
| Any expense message | Logs the transaction |
| `show spending` / `summary` | Weekly digest |
| `recent` / `last 5` | Last 5 transactions |
| `undo` / `delete last` | Remove last entry |

---

## Weekly Digest (Auto)

Every Sunday at 9 AM, you'll automatically receive:

```
📊 Weekly Spending Digest
Mar 17 – Mar 23, 2026

💰 Total: 12,450৳  (23 transactions)

📂 Top Categories:
  Remittance     5,000৳  (40%)
  Food           3,200৳  (26%)
  Utilities      1,200৳  (10%)
  Transport        950৳   (8%)

📱 Payment Methods:
  🔴 bKash:   8,200৳
  🟠 Nagad:   3,400৳
  💵 Cash:      850৳

💡 Remittance is your biggest expense this week.
   Consider timing transfers when BDT rates are favorable.
```

---

## Data Storage

All data is stored **locally** on your machine at:
```
~/.openclaw/bkash-nagad-tracker/transactions.json
```

No cloud sync. No third-party servers. Your financial
data never leaves your device.

---

## Requirements

- OpenClaw installed and running
- Python 3.10 or higher
- Anthropic API key (for smart parsing and digests)

---

## Privacy

This skill stores all data locally. The only external
API call is to Anthropic for natural language parsing
— no transaction data is stored by Anthropic beyond
the immediate API response.

---

## Built by

Built for the Bangladeshi diaspora and local users
who want simple, private expense tracking without
complex apps or bank API integrations.

**Author:** Your Name  
**ClawHub:** clawhub.ai/yourname/bkash-nagad-tracker  
**GitHub:** github.com/yourname/bkash-nagad-tracker
