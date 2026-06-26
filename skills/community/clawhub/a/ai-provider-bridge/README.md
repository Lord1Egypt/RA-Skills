# AI Provider Bridge

Unified interface for 6 AI providers. One function call, any model.

## Supported Providers

| Provider | Models | API Key Env Var |
|----------|--------|----------------|
| Anthropic | Claude Opus, Sonnet, Haiku | `ANTHROPIC_API_KEY` |
| OpenAI | GPT-4o, GPT-4, GPT-3.5 | `OPENAI_API_KEY` |
| Google | Gemini Pro, Gemini Flash | `GOOGLE_API_KEY` |
| xAI | Grok | `XAI_API_KEY` |
| Mistral | Mistral Large, Medium, Small | `MISTRAL_API_KEY` |
| Ollama | Any local model | None (local) |

## Usage

```javascript
const { AIBridge } = require('./src/ai-bridge');

const ai = new AIBridge({
  provider: 'anthropic',  // or 'openai', 'google', 'xai', 'mistral', 'ollama'
  model: 'claude-sonnet-4-20250514',
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await ai.chat('What is the capital of France?');
console.log(response);
```

## Switching Providers

Change the provider and model in config — no code changes needed:

```javascript
// Switch from cloud to local
ai.setProvider('ollama');
ai.setModel('llama3.1:8b');

// Same interface
const response = await ai.chat('Same question, free model');
```

## Zero Dependencies

Uses only Node.js built-in `https` and `http` modules. No npm install needed.
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
