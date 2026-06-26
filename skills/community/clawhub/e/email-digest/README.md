# EmailDigest — Daily Email Summary for Agents

Your agent checks your email. Surfaces what matters. Ignores what doesn't.

## What You Get

```
📬 Email Digest — Feb 28, 2026

URGENT (2):
• Boss wants Q4 numbers by EOD — received 7:23 AM
• Client contract expires tomorrow — needs signature

ACTION NEEDED (3):
• PR review requested on auth-module (#142)
• Meeting reschedule request from Sarah
• Invoice #4021 payment confirmation needed

FYI (8):
• 3 newsletter digests
• 2 shipping notifications
• GitHub: 3 new issues in your repos

Spam filtered: 12 messages
```

## Configuration

```yaml
accounts:
  - provider: gmail
    address: your@gmail.com

priority_senders:
  - boss@company.com
  - partner@email.com

urgency_keywords:
  - urgent
  - asap
  - deadline

ignore_senders:
  - noreply@*
  - marketing@*
```

## Features

- **Smart categorization** — urgent / action needed / FYI / ignorable
- **Priority sender highlighting** — configurable VIP list
- **Action item extraction** — pulls out what needs doing
- **Thread summarization** — long chains condensed to key points
- **Multiple accounts** — aggregate from Gmail, Outlook, any IMAP
- **Privacy** — all processing is local. Emails never leave your machine.
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
