# EnvGuard — Secret & Credential Scanner

Find leaked secrets before they reach production.

## Quick Scan

```bash
node src/env-guard.js scan ./my-project
```

## What It Finds

| Secret Type | Pattern |
|-------------|---------|
| API Keys | `sk-...`, `AKIA...`, `ghp_...` |
| Passwords | `password=`, `passwd:` |
| Tokens | `token=`, `bearer ...` |
| Private Keys | `-----BEGIN RSA PRIVATE KEY-----` |
| Connection Strings | `mongodb://`, `postgres://` |
| Webhook URLs | Discord webhooks, Slack webhooks |

## Features

- **Custom patterns** — add your own secret patterns
- **Allowlisting** — mark false positives to skip
- **CI integration** — exit code 1 for pipeline gates

## Output

```
🔴 SECRETS FOUND — 3 issues

src/config.js:12
  API key detected: sk-proj-...Tm4x (OpenAI)

.env.backup:3
  Database password in committed file

logs/debug.log:445
  Bearer token logged in plaintext
```
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
