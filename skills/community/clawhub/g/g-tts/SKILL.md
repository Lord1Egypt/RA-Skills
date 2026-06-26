---
name: g-tts
description: |
  High-definition generative speech synthesis using Google Cloud Chirp 3 HD voices. 
  Delivers superior realism, emotional expressiveness, and natural pacing using LLM-based generative audio models.
  Use when: (1) User requests audio/voice output with "tts" or "speak" triggers. (2) Content requires natural human-like prosody.
env:
  - OPENCLAW_WORKSPACE: "The directory where output audio files will be saved. Falls back to current working directory if not set."
requirements:
  - node: ">=18.0.0"
  - external_auth: "Google Application Default Credentials (ADC) via 'gcloud auth application-default login'"
  - network: "Required for first-run npm installation and Google API communication"
---

# Google Chirp 3 HD TTS Skill

## Overview

Generate ultra-realistic, human-like speech using Google's latest **Chirp 3 HD** generative models. This skill handles its own dependencies locally to remain portable.

> **Security Note:** On first execution, this skill will run `npm install` locally within its own folder to fetch the official `@google-cloud/text-to-speech` library from the public npm registry.

---

## Trigger Detection

Recognize keywords like **"tts"**, **"speak"**, **"voice"**, or **"read this out loud"** as TTS requests.
- **Action**: Extract the target text, strip the trigger keyword, apply "Natural Speech" formatting (see below), then call the tool using the auto-run logic below.

---

## Auto-Run Logic (Agent Instructions)

Follow these steps every time TTS is needed. Never assume `gtts` is in PATH — always run via `node` directly.

### Step 1 — Find the skill folder
`gtts.js` lives in the **same folder as this SKILL.md**. Resolve that path:

```bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
```

### Step 2 — Check Node.js (Version 18+ Required)

```bash
if ! command -v node &>/dev/null; then
    echo "ERROR: Node.js is not installed."
    exit 1
fi

NODE_MAJOR=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "ERROR: Node.js 18 or higher is required for Google Chirp 3 HD."
    exit 1
fi
```

### Step 3 — Auto-install dependency if missing
This installs the package **locally inside the skill folder** only.

```bash
if [ ! -d "$SKILL_DIR/node_modules/@google-cloud/text-to-speech" ]; then
    npm install @google-cloud/text-to-speech --prefix "$SKILL_DIR" --silent
fi
```

### Step 4 — Run the script

```bash
node "$SKILL_DIR/gtts.js" --text "$TEXT" --voice "$VOICE" --out "$OUTFILE"
```

---

## Command Arguments

| Argument | Description | Default |
| :--- | :--- | :--- |
| `--text` | Text to synthesize. Supports `[pause]` tags. | *(required)* |
| `--voice` | Voice short-name (e.g. Aoede, Charon, Puck) | `Aoede` |
| `--out` | Output filename (saved to $OPENCLAW_WORKSPACE) | `output.mp3` |

Returns `SUCCESS:/absolute/path/to/file.mp3` on success, or `ERROR: ...` on failure.

---

## Voice Selection

| Gender | Recommended HD Voices |
| :--- | :--- |
| **Female** | Achernar (Default), Aoede, Leda, Kore, Zephyr, Despina, Gacrux, Vindemiatrix |
| **Male** | Charon, Puck, Fenrir, Orus, Achird, Algenib, Enceladus |

---

## Prompt Engineering for Natural Speech

### 1. Pause Tags
Converted automatically into SSML `<break>` tags:

| Tag | Duration |
| :--- | :--- |
| `[pause short]` | 300ms |
| `[pause]` | 600ms |
| `[pause long]` | 900ms |

### 2. Human-Like Formatting
- **Contractions**: Use "I'm", "don't", "can't" for a conversational tone.
- **Ellipses**: Use `...` for trailing hesitation.
- **Fillers**: Use "Well,", "Um,", or "So," to mimic natural thought.

---

## Authentication

Uses **Google Application Default Credentials (ADC)**. One-time setup:

```bash
gcloud auth application-default login
```

---

## Requirements

| Requirement | Status |
| :--- | :--- |
| Node.js 18+ | ❌ Must be installed on system |
| OPENCLAW_WORKSPACE | ℹ️ Optional (Defaults to current dir) |
| `@google-cloud/text-to-speech` | ✅ Auto-installed locally in skill folder |
| Google Cloud SDK + ADC login | ❌ One-time manual step required |

---

## Workflow

1. **Detect Intent** — Identify a TTS trigger keyword.
2. **Format Text** — Apply contractions, ellipses, and `[pause]` tags.
3. **Check Environment** — Confirm `node` (18+) is available and `OPENCLAW_WORKSPACE` is known.
4. **Auto-install deps** — Run Step 3 if `node_modules` is missing.
5. **Execute** — `node "$SKILL_DIR/gtts.js" --text "..." --voice "..." --out "..."`
6. **Confirm Output** — Reference the `SUCCESS:` path and confirm to the user.
```