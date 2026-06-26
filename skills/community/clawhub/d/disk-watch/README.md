# DiskWatch — Disk Space Monitor & Alert

Get alerted before your disk fills up. Find what's eating space.

## Usage

```javascript
const { DiskWatch } = require('./src/disk-watch');
const watch = new DiskWatch({
  warningThreshold: 80,
  criticalThreshold: 90,
  checkInterval: 3600000  // hourly
});
watch.start();
```

## Output

```
💾 Disk Status

C: 234/500 GB (47%) ✅
D: 890/1000 GB (89%) ⚠️ WARNING
E: 58/64 GB (91%) 🔴 CRITICAL

Top consumers (D:):
  1. /data/backups/  312 GB (35%)
  2. /data/logs/     198 GB (22%)
  3. /data/models/   145 GB (16%)

Suggestion: backups/ has 187 GB reclaimable (>90 days old)
```

## Features

- **Multi-drive monitoring** — all mounted drives
- **Threshold alerts** — warning and critical levels
- **Space hog detection** — largest directories
- **Trend tracking** — "Disk growing 2 GB/day"
- **Cleanup suggestions** — old files, duplicates
- **Cross-platform** — Windows, Linux, macOS
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
