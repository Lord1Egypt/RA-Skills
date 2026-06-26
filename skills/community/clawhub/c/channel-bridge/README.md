# ChannelBridge — Cross-Platform Message Routing

Your agent lives on multiple platforms. ChannelBridge routes messages between them.

## Use Cases

- Forward Discord alerts to Slack
- Send email summaries to Telegram
- Cross-post announcements to all channels
- Route urgent messages to SMS/Signal

## Configuration

```yaml
routes:
  - name: "urgent-to-signal"
    from: discord
    filter: "contains:urgent OR from:boss"
    to: signal
    transform: "summarize"

  - name: "daily-digest"
    from: [email, discord, slack]
    schedule: "0 18 * * *"
    to: telegram
    transform: "digest"

  - name: "announcements"
    from: slack
    filter: "channel:#announcements"
    to: [discord, telegram, email]
    transform: "forward"
```

## Transforms

| Transform | What It Does |
|-----------|-------------|
| `forward` | Pass through as-is |
| `summarize` | Condense to key points |
| `digest` | Batch into daily summary |
| `translate` | Adapt formatting per platform |

## Platform Support

Works with any platform OpenClaw supports: Discord, Slack, Telegram, Signal, Email, WhatsApp, SMS.
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
