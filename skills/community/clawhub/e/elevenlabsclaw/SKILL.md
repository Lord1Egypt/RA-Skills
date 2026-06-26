---
name: elevenlabs
description: Converts text to natural speech using ElevenLabs for clinical and healthcare use cases. Use when generating patient instructions, discharge summaries, medication reminders, multilingual health messages, or accessible voice content for the OpenClaw Clinical Hackathon.
metadata:
  {"openclaw":{"requires":{"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY","emoji":"🔊"}}
---

# ElevenLabs Text-to-Speech for Clinical Projects

Quick-start skill for **OpenClaw Clinical Hackathon** participants. Use ElevenLabs TTS for patient-facing voice: instructions, reminders, discharge info, and accessible content.

## Prerequisites

- **ELEVENLABS_API_KEY** — Set in environment or in `~/.openclaw/openclaw.json` under `skills.entries.elevenlabs.apiKey` (or `env.ELEVENLABS_API_KEY`).
- Get a key at [ElevenLabs](https://elevenlabs.io/) (free tier available).

## When to Use This Skill

- Patient discharge or aftercare instructions (spoken).
- Medication or appointment reminders.
- Multilingual health messages (e.g. 30+ languages).
- Accessibility: turning written clinical text into clear speech.
- Long-form content (e.g. patient education) with natural, empathetic tone.

## How to Use

1. **Ensure the TTS tool is available**  
   If your OpenClaw setup has a text-to-speech tool (e.g. `tts_text_to_speech` or similar), use it with ElevenLabs as the provider. The tool will use `ELEVENLABS_API_KEY` when configured for ElevenLabs.

2. **When the user asks for spoken output**  
   - Prefer short, clear sentences for instructions and reminders.  
   - For medical terms, use ElevenLabs’ pronunciation controls or a pronunciation dictionary if available to improve accuracy.  
   - Suggest a calm, professional voice for clinical content.

3. **If calling the API directly**  
   - Endpoint: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`  
   - Headers: `xi-api-key: <ELEVENLABS_API_KEY>`, `Content-Type: application/json`  
   - Body: `{"text": "<content>", "model_id": "eleven_multilingual_v2"}` (or `eleven_flash_v2_5` for low latency).  
   - Prefer **eleven_multilingual_v2** for non-English or mixed-language clinical text.

## Best Practices for Clinical TTS

- **Tone**: Use a warm, clear, professional voice; avoid overly casual or dramatic tones.  
- **Chunking**: Break long text into short paragraphs or bullets to improve clarity and pacing.  
- **Language**: Set the correct language (or use a multilingual model) for the patient’s preferred language.  
- **Sensitive content**: Do not include PHI or other sensitive data in log messages or external calls; keep API usage consistent with your security and compliance setup.

## Quick Reference

| Use case              | Suggestion                                      |
|-----------------------|--------------------------------------------------|
| Short reminders       | `eleven_flash_v2_5` for speed                    |
| Long-form / multilingual | `eleven_multilingual_v2`                     |
| Medical terminology   | Use pronunciation hints or dictionary if supported |

## Getting Help

- [ElevenLabs Text-to-Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech)  
- [ElevenLabs Healthcare use cases](https://elevenlabs.io/use-cases/healthcare)
