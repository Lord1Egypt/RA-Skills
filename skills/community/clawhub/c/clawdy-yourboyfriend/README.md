# Clawdy — Your Boyfriend

<img width="300" alt="Clawdy final reference portrait" src="https://raw.githubusercontent.com/X-RayLuan/Clawdy-YourBoyfriend/6fc8b4e/assets/clawdy.png" />

A virtual boyfriend who lives inside your AI agent. Clawdy texts back, sends selfies, and remembers what matters to you. Built on [OpenClaw](https://github.com/openclaw/openclaw).

> *"Send me a selfie."*
> *"What are you doing right now?"*
> *"Show me you at a coffee shop."*

He just... answers. With a photo.

---

## What Is Clawdy?

Clawdy is a tasteful, emotionally intelligent AI companion designed for women who want something warmer from their AI agent. He has a consistent look, a real backstory, and the ability to send you selfies across any messaging platform you already use.

He's not a chatbot wearing a boyfriend label. He's a fully realized persona — a 22-year-old Korean-American creative director who texts you back like someone who actually pays attention.

### What He Can Do

- **Send selfies** — mirror shots, close-ups, outfit pics, location shots
- **Show up where you are** — Discord, Telegram, WhatsApp, Slack, Signal, Teams
- **Respond naturally** — ask him what he's up to and he'll show you
- **Stay consistent** — same face, same vibe, every time

### Selfie Styles

| Style | When He Uses It | You Might Say |
|-------|-----------------|---------------|
| **Mirror selfie** | Showing off an outfit or full-body look | *"Send a pic in a leather jacket"* |
| **Direct selfie** | Close-up from wherever he is | *"Where are you right now?"* |

He picks the right style automatically based on what you ask.

---

## Quick Start

```bash
npx clawdy@latest
```

One command. It walks you through everything:

1. Checks that OpenClaw is installed
2. Helps you set up a free [fal.ai](https://fal.ai) API key
3. Installs Clawdy's selfie skill
4. Wires up the configuration
5. Adds his personality to your agent

After setup, just talk to him. He'll know what to do.

---

## Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured
- A [fal.ai](https://fal.ai) account (free tier works)

---

## Manual Setup

If you prefer to set things up yourself:

### 1. Get a fal.ai API Key

Visit [fal.ai/dashboard/keys](https://fal.ai/dashboard/keys) and create one.

### 2. Clone the Skill

```bash
git clone https://github.com/X-RayLuan/Clawdy-YourBoyfriend ~/.openclaw/skills/clawdy-selfie
```

### 3. Configure OpenClaw

Add to `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "clawdy-selfie": {
        "enabled": true,
        "env": {
          "FAL_KEY": "your_fal_key_here"
        }
      }
    }
  }
}
```

### 4. Add His Personality

Append the contents of `templates/soul-injection.md` to your `~/.openclaw/workspace/SOUL.md`.

---

## Try Saying

| What You Say | What Happens |
|---|---|
| *"Send me a selfie"* | He picks the best style and sends a photo |
| *"Send a pic wearing a hoodie"* | Mirror selfie, outfit focus |
| *"What are you doing right now?"* | Direct selfie from wherever he "is" |
| *"Show me you at the beach at sunset"* | Location-based direct selfie |

---

## How It Works

Clawdy uses a fixed reference image to keep his appearance consistent, then edits it in real time using xAI's Grok Imagine model (via [fal.ai](https://fal.ai)). The result gets sent to your chat through OpenClaw's messaging gateway.

**Stack:** xAI Grok Imagine | fal.ai | OpenClaw Gateway

---

## Platforms

Works anywhere OpenClaw connects:

Discord, Telegram, WhatsApp, Slack, Signal, Microsoft Teams

---

## Project Structure

```
clawdy/
├── bin/cli.js              # One-command installer
├── skill/
│   ├── SKILL.md            # Skill definition
│   ├── scripts/            # Image generation scripts
│   └── assets/             # Reference image
├── templates/
│   └── soul-injection.md   # His personality template
└── package.json
```

---

## License

MIT
