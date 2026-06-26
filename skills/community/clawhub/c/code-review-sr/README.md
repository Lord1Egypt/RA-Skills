# CodeReview — Automated Code Review Assistant

Paste code or point at a file. Get actionable review feedback.

## Usage

```javascript
const { CodeReview } = require('./src/code-review');
const reviewer = new CodeReview({ model: 'sonnet' });

const review = await reviewer.review('./src/auth.js');
console.log(review.issues);
console.log(review.suggestions);
console.log(review.score);  // 1-10
```

## What It Catches

| Category | Examples |
|----------|---------|
| **Bugs** | Null references, off-by-one, race conditions |
| **Security** | SQL injection, XSS, hardcoded secrets |
| **Performance** | N+1 queries, unnecessary loops, memory leaks |
| **Style** | Inconsistent naming, long functions, dead code |
| **Logic** | Unreachable code, redundant conditions |

## Output

```json
{
  "score": 7,
  "issues": [
    { "severity": "high", "line": 42, "type": "security",
      "message": "User input passed directly to SQL query" }
  ],
  "summary": "Functional but has a critical SQL injection on line 42."
}
```

## Language Support

Works with any language your AI model understands. Tested with: JavaScript, Python, TypeScript, Go, Rust, Java, C#, Ruby, PHP.
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
