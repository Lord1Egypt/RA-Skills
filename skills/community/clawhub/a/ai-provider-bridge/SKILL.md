---
name: "AI Provider Bridge — Unified API for Anthropic/OpenAI/Google/xAI/Mistral/Ollama"
description: "One interface to call 6 AI providers. Swap models with a config change, not a code rewrite. Zero external dependencies."
author: "@TheShadowRose"
version: "1.0.3"
tags: ["api", "multi-provider", "anthropic", "openai", "google-gemini", "xai-grok", "mistral", "ollama", "abstraction-layer"]
license: "MIT"
env:
  ANTHROPIC_API_KEY: "Required for Anthropic/Claude models (optional if not using Anthropic)"
  OPENAI_API_KEY: "Required for OpenAI/GPT models (optional if not using OpenAI)"
  GOOGLE_API_KEY: "Required for Google/Gemini models (optional if not using Google)"
  XAI_API_KEY: "Required for xAI/Grok models (optional if not using xAI)"
  MISTRAL_API_KEY: "Required for Mistral models (optional if not using Mistral)"
---

# AI Provider Bridge — Unified API for Anthropic/OpenAI/Google/xAI/Mistral/Ollama

One interface to call 6 AI providers. Swap models with a config change, not a code rewrite. Zero external dependencies.

---

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
  currentModel: 'anthropic/claude-sonnet-4-20250514',
  anthropicApiKey: process.env.ANTHROPIC_API_KEY,  // only needed for Anthropic models
  openaiApiKey:    process.env.OPENAI_API_KEY,      // only needed for OpenAI models
  googleApiKey:    process.env.GOOGLE_API_KEY,      // only needed for Google models
  xaiApiKey:       process.env.XAI_API_KEY,         // only needed for xAI models
  mistralApiKey:   process.env.MISTRAL_API_KEY,     // only needed for Mistral models
  ollamaHost:      'http://127.0.0.1:11434'         // optional, default shown
});

const response = await ai.sendMessage('What is the capital of France?');
console.log(response);
```

## Switching Providers

Change the model — provider is inferred from the prefix:

```javascript
// Switch from cloud to local Ollama
ai.setModel('ollama/llama3.1:8b');

// Same interface
const response = await ai.sendMessage('Same question, free model');
```

**Model prefix → provider mapping:**
- `anthropic/` → Anthropic API
- `openai/` → OpenAI API
- `google/` → Google Gemini API
- `xai/` → xAI Grok API
- `mistral/` → Mistral API
- `ollama/` → Local Ollama (no API key needed)

## Zero Dependencies

Uses only Node.js built-in `https` and `http` modules. No npm install needed.
---

## Changelog

**v1.0.3**
- Fixed API usage examples — config object uses camelCase property names (`anthropicApiKey`, `openaiApiKey`, `googleApiKey`, `xaiApiKey`, `mistralApiKey`), not flat `apiKey` or env var names. Model prefix determines provider (`anthropic/model-name`). Clarified `sendMessage()` as the correct method name.

**v1.0.2**
- Removed `require('./token-compressor')` reference entirely. TokenCompressor is now an inlined no-op pass-through class — no missing dependency, no external file needed. To enable compression, install the companion token-compressor skill and swap the class as noted in the code comments.
- Removed automatic `"Do not store or train on this data."` appended to system prompts in OpenAI-compatible requests. This is the caller's responsibility — pass it via `setSystemPrompt()` if needed.

**v1.0.1**
- TokenCompressor dependency made optional — no-op fallback added when `./token-compressor` is not present. Bridge works without it; messages pass through uncompressed.
- Removed `buildSystemPrompt()` and `workspaceContext` option. These allowed embedding workspace files into system prompts sent to external APIs — data exposure risk. Use `setSystemPrompt()` directly.
- Added `env:` section to frontmatter declaring required API keys per provider. All optional — only keys for providers you use are needed.

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