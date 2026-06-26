---
name: cf-img-gen
description: "AI image generation via Cloudflare Workers AI (free tier, FLUX models) with optional prompt enhancement via Ollama or the primary LLM agent. Use when generating images from text prompts, creating visual assets, or when the user asks to generate/create an image. Triggers: 'generate image', 'create image', 'draw me', 'make an image', 'imagine', image generation requests. Zero cost on free tier (10K neurons/day)."
---

# CF Image Gen — Cloudflare Workers AI Image Generation

Free AI image generation using Cloudflare Workers AI, with optional prompt enhancement to refine and expand short prompts into detailed, vivid descriptions before generation.

**Two enhancement paths:**
1. **Primary LLM agent** — the calling AI agent (e.g. Jerith, running on OpenRouter/GPT/etc.) enhances the prompt before passing it to the skill. Higher quality, more creative, understands context.
2. **Ollama** — a local or remote Ollama LLM handles enhancement. Good for automation, no external API calls, works standalone.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Prompt Enhancement](#prompt-enhancement)
6. [Models](#models)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)
9. [File Layout](#file-layout)

---

## Prerequisites

Before using this skill, you need:

1. **A Cloudflare account** — Sign up at https://cloudflare.com (free tier is sufficient)
2. **Workers AI enabled** — Go to https://dash.cloudflare.com → Workers & Pages → Overview
3. **Node.js 18+** — Required to run the script
4. **Ollama (optional)** — For standalone prompt enhancement. Can be local or remote. Install at https://ollama.com

---

## Installation

### Step 1: Copy the skill to your workspace

Copy the `cf-img-gen` directory to your OpenClaw workspace skills folder:

```bash
cp -r cf-img-gen ~/.openclaw/workspace/skills/cf-img-gen
```

### Step 2: Create the credentials file

Copy the example env file and fill in your credentials:

```bash
# Create the credentials file
mkdir -p ~/.openclaw/workspace/ACCESS
cat > ~/.openclaw/workspace/ACCESS/cloudflare-workers-ai.env << 'EOF'
CF_WORKERS_AI_TOKEN=your_api_token_here
CF_WORKERS_AI_ACCOUNT=your_account_id_here
EOF

# Edit with your actual credentials
nano ~/.openclaw/workspace/ACCESS/cloudflare-workers-ai.env
```

### Step 3: Secure the credentials file

```bash
chmod 600 ~/.openclaw/workspace/ACCESS/cloudflare-workers-ai.env
```

### Step 4: Verify it works

```bash
cd ~/.openclaw/workspace/skills/cf-img-gen
node cf-img-gen.js "a test image of a blue circle" --width 512 --height 512
```

You should see output like:

```
🎨 Generating with flux-schnell (512x512)...
✅ Saved: /home/user/.openclaw/media/cf-img-gen/cf-img-1234567890.jpg

MEDIA:/home/user/.openclaw/media/cf-img-gen/cf-img-1234567890.jpg
```

---

## Configuration

### Cloudflare Credentials File

The skill reads Cloudflare credentials from `~/.openclaw/workspace/ACCESS/cloudflare-workers-ai.env`.

Create this file with the following format:

```
CF_WORKERS_AI_TOKEN=your_api_token_here
CF_WORKERS_AI_ACCOUNT=your_account_id_here
```

### Getting Your Cloudflare API Token

1. Log in to the Cloudflare dashboard: https://dash.cloudflare.com
2. Click your profile icon (top right) → **My Profile**
3. Go to **API Tokens** → **Create Token**
4. Use the **"Workers AI"** template or create a custom token with:
   - **Account** → **Workers AI** → **Edit** (minimum: Read)
5. Copy the token and paste it into the env file

### Getting Your Cloudflare Account ID

1. Log in to the Cloudflare dashboard: https://dash.cloudflare.com
2. Go to **Workers & Pages** → **Overview**
3. Your Account ID is displayed on the right side (alphanumeric string, ~32 characters)
4. Copy it and paste it into the env file

### Ollama Configuration (Optional)

Ollama prompt enhancement can use either a **local** or **remote** Ollama instance.

**Defaults (no configuration needed for local Ollama):**
- Host: `http://localhost:11434`
- Model: `llama3.2:3b`
- Timeout: `30000` ms

**Customizing Ollama connection:**

Via environment variables:
```bash
export OLLAMA_HOST=http://192.168.1.100:11434
export OLLAMA_MODEL=qwen2.5:7b
```

Via CLI flags:
```bash
node cf-img-gen.js "red panda" --ollama --ollama-host http://192.168.1.100:11434 --ollama-model qwen2.5:7b
```

Via API options (see [API Reference](#api-reference)).

**Setting up a remote Ollama server:**

If running Ollama on a different machine, ensure it's accessible:
```bash
# On the Ollama server, bind to all interfaces
OLLAMA_HOST=0.0.0.0 ollama serve
```

Then connect from your client:
```bash
node cf-img-gen.js "red panda" --ollama --ollama-host http://your-server-ip:11434
```

### Output Directory

Generated images are saved to: `~/.openclaw/media/cf-img-gen/`

The directory is created automatically on first run.

---

## Usage

### As a Module (Programmatic)

```javascript
const imgGen = require('./cf-img-gen');

// ── Basic usage (no enhancement) ──
const result = await imgGen.generate({ prompt: "a red panda in space" });

// ── With image options ──
const result = await imgGen.generate({
  prompt: "a cyberpunk city at night",
  width: 1024,
  height: 768,
  model: "flux-dev",
  steps: 8,
});

// ── With Ollama prompt enhancement (default local) ──
const result = await imgGen.generate({
  prompt: "red panda",
  ollama: true,
});

// ── With Ollama using custom model and remote host ──
const result = await imgGen.generate({
  prompt: "red panda",
  ollama: {
    host: "http://192.168.1.100:11434",
    model: "qwen2.5:7b",
    timeout: 30000,
  },
});

// ── With primary LLM agent enhancement ──
// (The calling LLM enhances the prompt before calling generate)
const enhancedPrompt = "A fluffy red panda sitting on a mossy branch in a misty forest, soft morning light filtering through the canopy, detailed fur texture, cinematic composition, 8K quality";
const result = await imgGen.generate({
  prompt: "red panda",
  llm: { enhancedPrompt },
});

// ── Check enhancement results ──
if (result.prompt.enhanced) {
  console.log("Original:", result.prompt.original);
  console.log("Enhanced:", result.prompt.enhanced);
  console.log("Source:", result.enhancement.source); // 'llm' or 'ollama'
}
```

### CLI

```bash
# Basic generation (default: 1024x1024, flux-schnell)
node cf-img-gen.js "a sunset over the ocean"

# Specify dimensions
node cf-img-gen.js "a mountain landscape" --width 1024 --height 768

# Use a different model
node cf-img-gen.js "a detailed portrait" --model flux-dev

# More inference steps for higher quality
node cf-img-gen.js "a complex scene" --model flux-dev --steps 8

# Enable Ollama prompt enhancement (default local model)
node cf-img-gen.js "red panda" --ollama

# Ollama with custom model
node cf-img-gen.js "red panda" --ollama --ollama-model qwen2.5:7b

# Ollama with remote host
node cf-img-gen.js "red panda" --ollama --ollama-host http://192.168.1.100:11434

# Provide a pre-enhanced prompt (from LLM agent)
node cf-img-gen.js "red panda" --enhanced-prompt "A fluffy red panda sitting on a mossy branch in a misty forest, soft morning light, detailed fur, cinematic"

# Combined: Ollama + custom model + image options
node cf-img-gen.js "red panda" --ollama --ollama-model llama3.2:3b --width 1024 --height 1024 --model flux-dev

# Show help
node cf-img-gen.js --help
```

### In OpenClaw / Discord (LLM Agent Usage)

When an LLM agent (like Jerith) handles image generation requests:

1. **Evaluate the user's prompt** — if it's short or vague, enhance it yourself
2. **Enhance the prompt** — expand it with visual details: lighting, composition, style, mood, colors, textures, atmosphere
3. **Call `generate()`** with the original prompt + your enhanced version via `llm.enhancedPrompt`
4. Return `MEDIA:<filepath>` for Discord auto-attach

**Example agent workflow:**

```
User: "draw me a red panda"

Agent thinks: "Short prompt — I should enhance it."
Enhanced: "A fluffy red panda sitting on a mossy branch in a misty bamboo forest, soft golden morning light filtering through the canopy, detailed fur texture with warm russet and cream tones, shallow depth of field, cinematic composition, peaceful atmosphere, 8K quality"

Agent calls:
  generate({
    prompt: "draw me a red panda",
    llm: { enhancedPrompt: "A fluffy red panda sitting on..." }
  })

Agent responds:
  🎨 Generated with flux-schnell (1024x1024) [llm enhanced]
  MEDIA:/path/to/image.jpg
```

**When to enhance:**
- Short prompts (1-4 words) — almost always enhance
- Vague prompts ("something cool", "make it pretty") — enhance with specifics
- Detailed prompts — pass through as-is, no enhancement needed
- User explicitly says "don't change my prompt" — skip enhancement

---

## Prompt Enhancement

### Enhancement Priority

When multiple enhancement options are provided, the skill uses this priority:

1. **`llm.enhancedPrompt`** — pre-enhanced by the primary LLM agent (highest priority)
2. **`ollama`** — Ollama LLM enhancement
3. **Original prompt** — no enhancement (fallback)

If `llm.enhancedPrompt` is provided, Ollama is skipped entirely. If `skipEnhance` is `true`, all enhancement is bypassed.

### Path 1: Primary LLM Agent Enhancement

The calling LLM agent (e.g. Jerith) enhances the prompt before calling `generate()`.

**Advantages:**
- Higher quality — the primary LLM is typically more capable than a small local model
- Context-aware — understands the conversation, user preferences, and intent
- Creative — can add artistic direction, references, and nuance
- No extra infrastructure — uses the agent that's already running
- No additional latency from a separate API call

**How to use:**
```javascript
// The agent enhances the prompt itself, then passes it
const result = await imgGen.generate({
  prompt: "red panda",
  llm: {
    enhancedPrompt: "A fluffy red panda in a misty forest, golden light, cinematic"
  },
});
```

**CLI equivalent:**
```bash
node cf-img-gen.js "red panda" --enhanced-prompt "A fluffy red panda in a misty forest, golden light, cinematic"
```

### Path 2: Ollama Enhancement

A local or remote Ollama LLM handles enhancement automatically.

**Advantages:**
- Works standalone — no need for the calling agent to enhance
- Consistent — same enhancement behavior every time
- Private — stays on your hardware (local Ollama)
- Good for automation — scripts and pipelines can use it without LLM agent involvement

**How to use:**
```javascript
const result = await imgGen.generate({
  prompt: "red panda",
  ollama: true,  // uses defaults
});

// Or with custom options
const result = await imgGen.generate({
  prompt: "red panda",
  ollama: {
    host: "http://192.168.1.100:11434",
    model: "qwen2.5:7b",
    timeout: 30000,
  },
});
```

### Graceful Degradation

If Ollama is unreachable (not running, network error, timeout), the skill falls back to the original prompt without throwing an error. A warning is logged to stderr. LLM agent enhancement has no failure mode — the agent either provides an enhanced prompt or doesn't.

### Recommended Ollama Models

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.2:3b` (default) | 3B | Fast | Good | General use, quick enhancement |
| `qwen2.5:7b` | 7B | Medium | Great | Better detail, creative prompts |
| `llama3.1:8b` | 8B | Medium | Great | Balanced quality/speed |
| `mistral:7b` | 7B | Medium | Good | Alternative to llama |

---

## Models

| Model | API Key | Speed | Quality | Best For |
|-------|---------|-------|---------|----------|
| FLUX.1 Schnell | `flux-schnell` | ~1-3s | Good | Quick generations, general use (default) |
| FLUX.1 Dev | `flux-dev` | ~5-10s | Great | Higher quality, more detail |
| Stable Diffusion XL | `sdxl` | ~3-5s | Good | SDXL-style outputs |
| DreamShaper 8 LCM | `dreamshaper` | ~2-4s | Good | Artistic/stylized images |

**Recommendation:** Use `flux-schnell` for quick iterations and general use. Switch to `flux-dev` with higher steps (6-8) for final/high-quality outputs.

---

## API Reference

### `generate(options)`

Generate an image from a text prompt, with optional prompt enhancement.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | *required* | Text description of the image to generate |
| `width` | number | 1024 | Image width in pixels |
| `height` | number | 1024 | Image height in pixels |
| `model` | string | `flux-schnell` | Model to use (see Models table) |
| `steps` | number | 4 | Number of inference steps (higher = more detail, slower) |
| `ollama` | `object\|true\|null` | `null` | Enable Ollama prompt enhancement. Pass `true` for defaults, or an object with `{ host, model, timeout }` |
| `llm` | `object\|null` | `null` | Pre-enhanced prompt from the primary LLM agent. Object with `{ enhancedPrompt: "..." }` |
| `skipEnhance` | boolean | `false` | If true, skip all prompt enhancement |

**Enhancement priority:** `llm.enhancedPrompt` > `ollama` > original prompt

**Ollama options (when `ollama` is an object):**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `host` | string | `http://localhost:11434` | Ollama server URL (local or remote) |
| `model` | string | `llama3.2:3b` | Ollama model to use for enhancement |
| `timeout` | number | `30000` | Request timeout in milliseconds |

**Returns:** `Promise<object>`

```javascript
{
  filepath: "/home/user/.openclaw/media/cf-img-gen/cf-img-1234567890.jpg",
  source: "cloudflare-workers-ai",
  model: "flux-schnell",
  width: 1024,
  height: 1024,
  cost: 0,
  size: 184320,           // bytes
  prompt: {
    original: "red panda",
    enhanced: "A fluffy red panda sitting on a mossy branch...",  // null if not enhanced
    used: "A fluffy red panda sitting on a mossy branch..."
  },
  enhancement: {
    source: "llm",           // 'llm' or 'ollama' (null if not enhanced)
    ollama: null,            // { host, model } if Ollama was used, else null
    llm: {
      note: "Enhanced by primary LLM agent before calling generate()"
    }  // null if LLM was not used
  }
}
```

**Throws:** Error if prompt is missing, credentials are invalid, or Cloudflare API request fails. Ollama failures are non-fatal (falls back to original prompt).

### `enhancePromptOllama(prompt, options)`

Standalone function to enhance a prompt via Ollama without generating an image.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | *required* | Original prompt to enhance |
| `options.host` | string | `http://localhost:11434` | Ollama server URL |
| `options.model` | string | `llama3.2:3b` | Ollama model to use |
| `options.timeout` | number | `30000` | Request timeout in ms |

**Returns:** `Promise<string>` — The enhanced prompt (or original on failure).

### `MODELS`

Object mapping model names to Cloudflare API identifiers:

```javascript
{
  'flux-schnell': '@cf/black-forest-labs/flux-1-schnell',
  'flux-dev': '@cf/black-forest-labs/flux-1-dev',
  'sdxl': '@cf/stabilityai/stable-diffusion-xl-base-1.0',
  'dreamshaper': '@cf/lykon/dreamshaper-8-lcm',
}
```

---

## Troubleshooting

### "Missing ACCESS/cloudflare-workers-ai.env"

The credentials file doesn't exist at `~/.openclaw/workspace/ACCESS/cloudflare-workers-ai.env`. Create it from the example file:

```bash
cp skills/cf-img-gen/cloudflare-workers-ai.env.example \
   ~/.openclaw/workspace/ACCESS/cloudflare-workers-ai.env
# Then edit with your credentials
```

### "CF_WORKERS_AI_TOKEN not found in env file"

The env file exists but doesn't contain the expected variables. Ensure the file has:

```
CF_WORKERS_AI_TOKEN=your_token
CF_WORKERS_AI_ACCOUNT=your_account_id
```

No quotes, no extra spaces around `=`.

### "Cloudflare API error: Authentication error"

Your API token is invalid or doesn't have Workers AI permissions. Check:
1. The token is copied correctly (no extra whitespace)
2. The token has Workers AI permissions (Account → Workers AI → Edit or Read)
3. Your Account ID matches the account the token was created on

### "Cloudflare API error: HTTP 429"

You've hit the rate limit. The free tier allows ~10K neurons/day. Wait a moment and try again.

### "No image in response"

The API returned a 200 but without image data. This can happen with:
- Invalid model names
- Prompts that trigger content filters
- Temporary Cloudflare API issues

Try again with a different prompt or model.

### Ollama: "Ollama unavailable"

Ollama prompt enhancement failed. The skill will fall back to the original prompt. To fix:
1. Ensure Ollama is running: `ollama serve`
2. Pull the model: `ollama pull llama3.2:3b`
3. For remote Ollama, verify the host URL is reachable
4. Check firewall rules if using a remote Ollama instance

### Ollama: "Ollama returned empty response"

The Ollama model returned an empty or malformed response. Try:
- A different model (e.g., `qwen2.5:7b` instead of `llama3.2:3b`)
- Increasing the timeout for slower models/servers
- Checking Ollama logs for model errors

### Request timeout

Large images or high step counts can take longer. The Cloudflare timeout is set to 120 seconds. The Ollama timeout defaults to 30 seconds (configurable via `--ollama-timeout` or `ollama.timeout`).

---

## File Layout

```
cf-img-gen/
├── cf-img-gen.js                     # Main module (CLI + programmatic API)
├── SKILL.md                          # This file — installation and usage guide
├── cloudflare-workers-ai.env.example # Template for credentials
└── CHANGELOG.md                      # Version history
```

Output images are stored separately:

```
~/.openclaw/media/cf-img-gen/
├── cf-img-1700000000000.jpg
├── cf-img-1700000001000.jpg
└── ...
```
