# ElevenLabs Audio & Music Skill for OpenClaw Clinical Hackathon

A [ClawHub](https://clawhub.ai/) skill that adds **ElevenLabs text-to-speech** and **Eleven Music (text-to-music)** to your OpenClaw agent for clinical and healthcare projects. Built for participants of the **OpenClaw Clinical Hackathon** who want to deliver patient-facing voice content—instructions, reminders, discharge information, accessible messaging, and **music therapy soundscapes**—with minimal setup.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Getting an ElevenLabs API Key](#getting-an-elevenlabs-api-key)
- [Usage](#usage)
- [Clinical Use Cases](#clinical-use-cases)
- [Music Therapy & Eleven Music](#music-therapy--eleven-music)
- [Models and Voices](#models-and-voices)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Publishing to ClawHub](#publishing-to-clawhub)
- [Project Structure](#project-structure)
- [Resources and Links](#resources-and-links)
- [License](#license)

---

## Overview

This skill teaches your OpenClaw agent **when** and **how** to use:

- The [ElevenLabs Text-to-Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech) for healthcare scenarios, and
- The [Eleven Music API](https://elevenlabs.io/docs/capabilities/music) to generate music from natural language prompts.

Once installed and configured with an API key, the agent can:

- Generate natural, human-like speech from clinical text (discharge instructions, medication reminders, patient education).
- Support **30+ languages** for multilingual patient communication.
- Create **music therapy soundscapes** and background tracks via text-to-music (relaxation, focus, sleep, stress reduction).
- Use low-latency or high-quality models depending on the use case (short reminders vs. long-form content).
- Follow clinical best practices: clear pronunciation, professional tone, and guidance on handling sensitive content and generative media.

The skill is **gated** on the `ELEVENLABS_API_KEY` environment variable: OpenClaw only loads and exposes it when the key is present, so you can install the skill in any workspace and enable it per agent or environment.

---

## Features

- **Agent instructions** — The skill’s `SKILL.md` tells the agent when to use TTS (e.g. “read this to the patient,” “generate a spoken reminder”) and how to call the ElevenLabs API or use an existing TTS tool configured for ElevenLabs.
- **Clinical focus** — Guidance tuned for healthcare: empathetic tone, clear medical terminology, chunking for clarity, and avoiding PHI in logs or external calls.
- **Model selection** — References to `eleven_multilingual_v2` (quality, long-form, many languages) and `eleven_flash_v2_5` (low latency for short prompts).
- **OpenClaw integration** — Uses standard skill metadata (`metadata.openclaw.requires.env`, `primaryEnv`) so the skill appears in the agent’s context only when `ELEVENLABS_API_KEY` is set.
- **ClawHub-ready** — Structured so you can publish to [ClawHub](https://clawhub.ai/) for discovery and one-command install (`clawhub install elevenlabs`).

---

## Prerequisites

- **OpenClaw** — An OpenClaw workspace or installation where skills are loaded (e.g. from `./skills` or `~/.openclaw/skills`). See [OpenClaw documentation](https://docs.openclaw.ai/).
- **ElevenLabs account** — A free or paid account at [elevenlabs.io](https://elevenlabs.io/) to obtain an API key.
- **Optional: ClawHub CLI** — If you install from ClawHub: `npm i -g clawhub` (or `pnpm add -g clawhub`). See [ClawHub docs](https://docs.openclaw.ai/tools/clawhub).

---

## Installation

### Option 1: Install from ClawHub (if published)

```bash
clawhub install elevenlabs
```

This installs the skill into your workspace’s `./skills` directory (or your configured OpenClaw workspace). Restart or start a new OpenClaw session so the agent picks up the skill.

### Option 2: Clone this repository

```bash
git clone https://github.com/arunnadarasa/elevenlabsclaw.git
cp -r elevenlabsclaw /path/to/your/openclaw/workspace/skills/elevenlabs
```

Replace `/path/to/your/openclaw/workspace` with your actual OpenClaw workspace path. The skill folder name under `skills/` should be `elevenlabs` to match the skill `name` in `SKILL.md`.

### Option 3: Manual copy

1. Create a folder `elevenlabs` inside your OpenClaw skills directory (e.g. `./skills/elevenlabs` or `~/.openclaw/skills/elevenlabs`).
2. Copy `SKILL.md` (and optionally `README.md`, `LICENSE`) into that folder.

After any method, set `ELEVENLABS_API_KEY` (see [Configuration](#configuration)) and start a new agent session.

---

## Configuration

The skill only loads when OpenClaw can resolve **ELEVENLABS_API_KEY**. You can provide it in two ways.

### 1. Environment variable

Export the key in the shell that runs OpenClaw:

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

Or add it to your `.env` or profile if your OpenClaw setup reads from there.

### 2. OpenClaw config (`~/.openclaw/openclaw.json`)

Inject the key via the skills entry for `elevenlabs`:

```json
{
  "skills": {
    "entries": {
      "elevenlabs": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "ELEVENLABS_API_KEY" }
      }
    }
  }
}
```

Or pass the key value directly (prefer env or vault in production):

```json
{
  "skills": {
    "entries": {
      "elevenlabs": {
        "enabled": true,
        "env": {
          "ELEVENLABS_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

- **enabled**: Set to `false` to disable the skill even when the key is present.
- **apiKey**: Uses OpenClaw’s secret resolution; `id` can point at an env var or vault key.
- **env**: Injected into the agent run; use for non-secret config if needed.

See [OpenClaw Skills documentation](https://docs.openclaw.ai/skills) for full options (e.g. `config`, per-skill overrides).

---

## Getting an ElevenLabs API Key

1. Go to [elevenlabs.io](https://elevenlabs.io/) and sign up or log in.
2. Open your **Profile** or **Settings** and find **API Key** (or go to the [API section](https://elevenlabs.io/app/settings/api-keys) of the ElevenLabs app).
3. Create a new API key and copy it. Store it securely (e.g. in a password manager or secret store); do not commit it to version control.
4. Set it as `ELEVENLABS_API_KEY` in your environment or in `~/.openclaw/openclaw.json` as shown in [Configuration](#configuration).

Free tier includes a limited number of characters per month; sufficient for hackathon demos and light use. For production or high volume, check [ElevenLabs pricing](https://elevenlabs.io/pricing).

---

## Usage

Once the skill is installed and `ELEVENLABS_API_KEY` is set:

1. **Start a new OpenClaw session** so the agent loads the skill.
2. Ask the agent to produce **spoken** or **voice** output for clinical content, for example:
   - “Convert these discharge instructions into speech for the patient.”
   - “Generate a short spoken reminder for taking medication at 8 AM.”
   - “Read this patient education paragraph in Spanish using ElevenLabs.”
3. The agent will use the instructions in `SKILL.md` to decide when to call the ElevenLabs API (or your TTS tool configured for ElevenLabs) and with which model/voice.

If your OpenClaw setup exposes a **TTS tool** (e.g. `tts_text_to_speech`) that is configured to use ElevenLabs, the skill instructs the agent to prefer that tool and pass the key via your existing config. Otherwise, the agent may call the ElevenLabs HTTP API directly using the key from the environment.

---

## Clinical Use Cases

| Use case | Description | Suggested model |
|----------|-------------|-----------------|
| **Discharge / aftercare** | Spoken instructions for the patient to follow at home. | `eleven_multilingual_v2` for clarity and natural pacing. |
| **Medication reminders** | Short, clear reminders (e.g. “Take your medication at 8 AM with food”). | `eleven_flash_v2_5` for low latency. |
| **Appointment reminders** | Time, place, and preparation instructions. | `eleven_flash_v2_5` or `eleven_multilingual_v2` depending on length. |
| **Multilingual messaging** | Instructions or education in the patient’s preferred language. | `eleven_multilingual_v2` (30+ languages). |
| **Accessibility** | Turning written clinical text into speech for visually impaired or low-literacy patients. | `eleven_multilingual_v2` with a clear, professional voice. |
| **Patient education** | Long-form explanations (e.g. condition overview, treatment options). | `eleven_multilingual_v2`; chunk long text for better pacing. |

Always ensure your usage complies with your organization’s privacy and security policies (e.g. no PHI in logs or in prompts sent to third-party APIs unless explicitly allowed).

---

## Music Therapy & Eleven Music

In addition to speech, this skill can guide your agent to use **Eleven Music** to generate music for **digital music therapy experiences**, relaxation, and patient engagement. Eleven Music turns natural language prompts into studio-grade music using the [Compose Music API](https://elevenlabs.io/docs/api-reference/music/compose) and related endpoints.[1](https://elevenlabs.io/docs/capabilities/music)[2](https://elevenlabs.io/docs/api-reference/music/compose)

### What you can build

- **Relaxation soundscapes** — Gentle ambient tracks to reduce anxiety before procedures or during waiting-room experiences.
- **Focus music** — Soft, non-distracting background music for rehabilitation exercises or cognitive training tasks.
- **Sleep support tracks** — Slow, calming pieces for bedtime routines in pediatric or chronic-care settings.
- **Guided therapy backing tracks** — Background music for mindfulness, breathing exercises, or guided imagery scripts.

### Music API (high-level)

- **Endpoint (compose):** `POST https://api.elevenlabs.io/v1/music`[2](https://elevenlabs.io/docs/api-reference/music/compose)  
- **Model:** `music_v1` (subject to change; see official docs).  
- **Prompt types:**  
  - Simple natural language prompt (\"calm piano ambient track for relaxation in a hospital room\").  
  - Structured composition plan (sections, intensity curves, etc.).  
- **Key parameters (examples):**  
  - `music_length_ms` — Duration (e.g. 60,000–180,000 ms for 1–3 minute tracks).  
  - `force_instrumental` — `true` for instrumental-only music (often preferred in clinical contexts).  
  - `seed` — For reproducible generations across sessions.  
  - `output_format` — e.g. MP3/PCM; choose based on your playback surface.

**Note:** Eleven Music access may require a **paid ElevenLabs plan**.[3](https://elevenlabs.io/docs/cookbooks/music/quickstart) Check your account’s plan and quotas before relying on it in demos.

### Example prompts for music therapy

- \"Create a 3-minute instrumental ambient track with soft piano and subtle strings to help an adult patient relax before an MRI scan.\"  
- \"Generate a calm, uplifting lo-fi track for pediatric physical therapy sessions—no vocals, gentle tempo.\"  
- \"Compose a slow, soothing lullaby-style piece for helping children fall asleep in a hospital ward.\"  
- \"Create a 10-minute meditative soundscape with ocean-like white noise and slow evolving pads for a mindfulness exercise.\"

When designing music therapy experiences, coordinate with clinical mentors or domain experts to ensure that tempo, intensity, and style align with your therapeutic goals and patient population.\n

---

## Models and Voices

The skill references two main ElevenLabs model IDs:

- **`eleven_flash_v2_5`** — Very low latency (~75 ms); good for short, real-time prompts (reminders, alerts).
- **`eleven_multilingual_v2`** — High quality, expressive, many languages; good for discharge instructions, education, and non-English content.

Voice IDs are chosen at runtime (by the agent or your tool). You can list available voices via the [ElevenLabs Voices API](https://elevenlabs.io/docs/api-reference/voices) or in the ElevenLabs dashboard. For clinical use, prefer voices that sound clear, calm, and professional.

**API endpoint (reference):**  
`POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`  
Headers: `xi-api-key: <ELEVENLABS_API_KEY>`, `Content-Type: application/json`  
Body: `{"text": "<content>", "model_id": "eleven_multilingual_v2"}` (or `eleven_flash_v2_5`).

Full details: [ElevenLabs Text-to-Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech).

---

## Best Practices

- **Tone** — Use a warm, clear, professional voice; avoid overly casual or dramatic delivery for clinical content.
- **Chunking** — Break long text into short paragraphs or bullets so the agent (and TTS) can pace the speech clearly.
- **Language** — Set the correct language in the request when using multilingual models so pronunciation and prosody match the target language.
- **Medical terms** — Use ElevenLabs’ pronunciation dictionary or hints where available to improve accuracy for drug names and clinical terms.
- **Sensitive data** — Do not include PHI or other sensitive data in logs, error messages, or in prompts sent to third-party APIs unless your compliance and security policies allow it. Prefer server-side or sandboxed execution when handling real patient data.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| **Skill not loading** | Ensure `ELEVENLABS_API_KEY` is set in the environment or in `skills.entries.elevenlabs` in `~/.openclaw/openclaw.json`. Restart the OpenClaw session after changing config. |
| **Agent doesn’t use TTS** | Phrase requests explicitly (“convert to speech,” “read aloud,” “generate voice version”). Confirm the skill is in `./skills/elevenlabs` (or your configured skills path) and that the skill name in `SKILL.md` is `elevenlabs`. |
| **401 Unauthorized** | API key is missing, wrong, or revoked. Regenerate the key in the ElevenLabs dashboard and update `ELEVENLABS_API_KEY`. |
| **Rate limits / quota** | Free tier has character limits. Check [ElevenLabs usage](https://elevenlabs.io/app/usage) and consider shorter prompts or a paid plan for demos. |
| **Wrong language or voice** | Specify `language_code` or the correct voice ID in the API request. The agent follows `SKILL.md`; you can extend the skill with explicit voice/language examples if needed. |

---

## Publishing to ClawHub

To publish this skill to [ClawHub](https://clawhub.ai/) so others can install it with `clawhub install elevenlabs`:

1. Install the ClawHub CLI: `npm i -g clawhub` (or `pnpm add -g clawhub`).
2. Log in: `clawhub login`.
3. From the repository root (where `SKILL.md` and `README.md` live), run:

```bash
clawhub publish . --slug elevenlabs --name "ElevenLabs TTS (Clinical)" --version 1.0.0 --tags latest,clinical,hackathon
```

- **--slug** — Identifier used for `clawhub install <slug>`.
- **--name** — Display name in the ClawHub UI.
- **--version** — Semver (e.g. `1.0.0`). Bump for updates (`1.0.1`, `1.1.0`, etc.).
- **--tags** — Tags for discovery (e.g. `clinical`, `hackathon`, `tts`).

To publish updates, bump the version and run `clawhub publish` again with the new `--version` and optional `--changelog "Description of changes"`.

---

## Project Structure

```
elevenlabsclaw/
├── README.md       # This file
├── SKILL.md        # OpenClaw skill definition (frontmatter + instructions)
└── LICENSE         # MIT
```

- **SKILL.md** — Required. Contains YAML frontmatter (`name`, `description`, `metadata.openclaw`) and the body that teaches the agent when and how to use ElevenLabs TTS. OpenClaw and ClawHub read this file to load and index the skill.

---

## Resources and Links

- [ElevenLabs Text-to-Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech) — API reference.
- [ElevenLabs Healthcare use cases](https://elevenlabs.io/use-cases/healthcare) — Product overview for healthcare.
- [OpenClaw Skills](https://docs.openclaw.ai/skills) — How OpenClaw loads and gates skills.
- [ClawHub](https://docs.openclaw.ai/tools/clawhub) — Skill registry and CLI (search, install, publish).
- [OpenClaw Clinical Hackathon](https://github.com/arunnadarasa/elevenlabsclaw) — This repo’s context.

---

## License

MIT. See [LICENSE](LICENSE) in this repository.
