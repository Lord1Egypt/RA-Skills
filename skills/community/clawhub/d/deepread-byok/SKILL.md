---
name: deepread-byok
title: DeepRead BYOK
description: Bring Your Own Key to DeepRead. Connect your OpenAI, Google, or OpenRouter API key — all document processing routes through YOUR account at zero DeepRead LLM cost. Page quota skipped entirely. Same API, same endpoints, one toggle.
metadata: {"openclaw":{"requires":{"env":["DEEPREAD_API_KEY"]},"primaryEnv":"DEEPREAD_API_KEY","homepage":"https://www.deepread.tech"}}
---

# DeepRead BYOK — Bring Your Own AI Key

Use your own OpenAI, Google, or OpenRouter API key for all DeepRead document processing. Your key, your billing, zero DeepRead LLM costs.

```
Without BYOK:  You → DeepRead API → DeepRead pays OpenRouter → You pay DeepRead
With BYOK:     You → DeepRead API → YOUR key pays provider   → DeepRead cost = $0
```

**Page quota is skipped entirely for BYOK users.** Process unlimited pages on any plan.

> **What this skill does and what it touches:** This skill helps agents guide users through BYOK setup. The agent opens the DeepRead dashboard (`https://www.deepread.tech/dashboard/byok`) in the user's browser so the user can paste their provider key directly into DeepRead's UI. It does not collect, store, or transmit provider keys itself. The `DEEPREAD_API_KEY` is read from the user's environment — this skill does not modify any system files, shell profiles, or `.env` files.

## What Changes With BYOK

- **LLM costs**: You pay your provider directly instead of DeepRead
- **Page quota**: **Skipped entirely** — no monthly limit when using your own key
- **API calls**: Same endpoints, same headers — zero code changes
- **Processing quality**: Equivalent models from your provider via tier-based swapping
- **Setup**: One-time — add your provider key in the dashboard, then forget about it

## Supported Providers

- **OpenRouter** (`sk-or-...`) — Easiest setup. Same models DeepRead uses, just swaps billing to your account.
- **OpenAI** (`sk-proj-...`) — Direct to `api.openai.com`. Best for enterprise agreements and negotiated rates.
- **Google** (`AI...`) — Direct to Google AI API. Best for Google Cloud credits and existing billing.

## Setup Guide

### Step 1: Get Your DeepRead API Key

You need a DeepRead account first. Sign up at https://www.deepread.tech/dashboard/?utm_source=clawhub (free, no credit card, 2,000 pages/month).

For automated agent setup with OAuth device flow, install the dedicated skill:

```bash
clawhub install uday390/deepread-agent-setup
```

That skill handles authentication securely. Once you have your DeepRead API key, set it as an environment variable in your shell or a secrets manager:

```bash
export DEEPREAD_API_KEY="sk_live_your_key_here"
```

### Step 2: Add Your Provider Key in the Dashboard

BYOK keys are managed through the DeepRead dashboard:

```bash
open "https://www.deepread.tech/dashboard/byok?utm_source=clawhub"
```

In the dashboard:

1. Click **Add Provider Key**
2. Select your provider — OpenRouter, OpenAI, or Google
3. Paste your API key
4. The key is validated against the provider's API before saving
5. The key is encrypted at rest and stored securely

That's it. All subsequent API calls automatically route through your key.

### Step 3: Process Documents (Same API as Before)

Nothing changes in your code. Same endpoints, same `X-API-Key` header:

```bash
DR_API_KEY=$(grep ^DEEPREAD_API_KEY .env | cut -d= -f2)

curl -X POST https://api.deepread.tech/v1/process \
  -H "X-API-Key: $DR_API_KEY" \
  -F "file=@document.pdf"
```

Under the hood, LLM calls now route through YOUR provider key. Page quota is NOT counted.

## Managing Your Key

All key management is done in the dashboard at https://www.deepread.tech/dashboard/byok

- **Toggle on/off**: Switch between your key and DeepRead processing without deleting the key
- **Replace**: Add a new key to replace the existing one (one active key at a time)
- **Delete**: Permanently removes the key, reverts to DeepRead processing

## How Model Swapping Works

When you provide an OpenAI or Google key, DeepRead automatically swaps all pipeline models to equivalents from your provider at the same quality tier:

**Top tier** — GPT-5 (OpenAI) or Gemini 2.5 Flash (Google)

**High tier** — GPT-5 Mini (OpenAI) or Gemini 2.5 Flash (Google)

**Mid tier** — GPT-5 Nano (OpenAI) or Gemini 3 Flash (Google)

**Lite tier** — GPT-5 Nano (OpenAI) or Gemini 2.5 Flash Lite (Google)

**OpenRouter users**: No swapping needed — same models, your billing account.

## Python Example

```python
import requests
import time

# Once BYOK is enabled in the dashboard, your existing code just works.
# LLM costs go to YOUR provider account. Page quota is not counted.

API_KEY = "sk_live_YOUR_KEY"
BASE = "https://api.deepread.tech"
headers = {"X-API-Key": API_KEY}

# Submit document — same API call as always
with open("invoice.pdf", "rb") as f:
    job = requests.post(
        f"{BASE}/v1/process",
        headers=headers,
        files={"file": f},
        data={"schema": '{"type":"object","properties":{"vendor":{"type":"string"},"total":{"type":"number"}}}'}
    ).json()

job_id = job["id"]
print(f"Job {job_id} — LLM costs go to your provider account")

# Poll for results
delay = 3
while True:
    time.sleep(delay)
    result = requests.get(f"{BASE}/v1/jobs/{job_id}", headers=headers).json()
    if result["status"] == "completed":
        print(f"Extracted: {result['structured_data']}")
        break
    elif result["status"] == "failed":
        print(f"Failed: {result['error']}")
        break
    delay = min(delay * 1.5, 15)
```

## JavaScript Example

```javascript
// Once BYOK is enabled in the dashboard, your existing code just works.

const API_KEY = "sk_live_YOUR_KEY";
const BASE = "https://api.deepread.tech";

const form = new FormData();
form.append("file", fs.createReadStream("invoice.pdf"));

const { id: jobId } = await fetch(`${BASE}/v1/process`, {
  method: "POST",
  headers: { "X-API-Key": API_KEY },
  body: form,
}).then(r => r.json());

console.log(`Job ${jobId} — LLM costs go to your provider account`);

let delay = 3000;
let result;
do {
  await new Promise(r => setTimeout(r, delay));
  result = await fetch(`${BASE}/v1/jobs/${jobId}`, {
    headers: { "X-API-Key": API_KEY },
  }).then(r => r.json());
  delay = Math.min(delay * 1.5, 15000);
} while (!["completed", "failed"].includes(result.status));
```

## Security

- **Encrypted at rest** — Fernet symmetric encryption (AES-128-CBC + HMAC-SHA256)
- **Validated before storing** — test API call to your provider confirms the key works
- **Key hints only** — dashboard shows only the last 4 characters for identification
- **Separate encryption key** — encryption key stored separately from the database
- **Soft-delete** — removing a key clears the ciphertext from the database
- **One key at a time** — simple billing, all processing routes through one provider

## Key Storage Best Practices

- **Use scoped or test keys** for development — most providers (OpenAI, Google) allow restricted-scope or short-lived keys
- **Use a secrets manager** for production (1Password CLI, OS keychain, AWS Secrets Manager, HashiCorp Vault) over plaintext storage
- **Rotate keys regularly** and revoke unused ones at https://www.deepread.tech/dashboard
- **Never commit** API keys to version control or share them in chat, screenshots, or logs
- **Verify the provider** — review DeepRead's privacy policy at https://www.deepread.tech before submitting your provider keys

DeepRead validates provider keys against the provider's API before encrypting and storing them. Keys are encrypted at rest and never logged.

## When to Use BYOK

**Use BYOK if:**

- You have an OpenAI enterprise agreement with negotiated rates
- You have Google Cloud credits you want to apply to document processing
- You want zero DeepRead LLM costs and unlimited page processing
- You need all AI calls to go through your own provider account for compliance
- You're on the free tier and want to skip the 2,000 page/month limit

**Don't use BYOK if:**

- You're happy with DeepRead's default processing — it works great out of the box
- You don't have an existing AI provider account
- You want DeepRead to handle all billing in one invoice

## Works With All DeepRead Skills

BYOK applies to every DeepRead API call — OCR, form fill, and PII redaction:

- **deepread-ocr** — Extract text and structured JSON from documents — `clawhub install uday390/deepread-ocr`
- **deepread-form-fill** — Fill any PDF form with AI vision — `clawhub install uday390/deepread-form-fill`
- **deepread-pii** — Redact sensitive data from documents — `clawhub install uday390/deepread-pii`
- **deepread-agent-setup** — Authenticate via OAuth device flow — `clawhub install uday390/deepread-agent-setup`
- **deepread-byok** — Set up Bring Your Own Key (this skill) — `clawhub install uday390/deepread-byok`

## Support

- **Dashboard**: https://www.deepread.tech/dashboard
- **BYOK Settings**: https://www.deepread.tech/dashboard/byok
- **Issues**: https://github.com/deepread-tech/deep-read-service/issues
- **Email**: hello@deepread.tech

---

**Ready?** Add your provider key at https://www.deepread.tech/dashboard/byok
