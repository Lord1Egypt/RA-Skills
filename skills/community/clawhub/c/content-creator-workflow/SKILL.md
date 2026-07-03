---
name: content-creator-workflow
description: Multi-modal content creation workflow for freelance creators. Receives customer requests via WhatsApp (text or voice note), transcribes audio with the OpenAI Whisper API, generates images with DALL-E 3, and replies to the customer with the result. Use to automate end-to-end request-to-image delivery.
homepage: https://platform.openai.com/docs/api-reference
tags: ['content-creation', 'whatsapp', 'whisper', 'dall-e', 'automation', 'workflow']
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires":
          { "bins": ["python3"], "env": ["OPENAI_API_KEY"] },
        "primaryEnv": "OPENAI_API_KEY",
        "install":
          [
            {
              "id": "python-brew",
              "kind": "brew",
              "formula": "python",
              "bins": ["python3"],
              "label": "Install Python (brew)",
            },
          ],
      },
  }
---

# Content Creator Workflow

Automates the full freelance content-creation loop: a customer sends a request
over WhatsApp (text or voice note), the workflow transcribes any audio, turns
the prompt into an image, and sends the result back.

## Pipeline

1. **wacli** — list/send WhatsApp messages (mock CLI; swap in a real backend).
2. **transcribe** — OpenAI Whisper API, with large-file chunking.
3. **generate_images** — DALL-E 3 image generation with safe filenames.
4. **workflow** — ties the steps together and replies to the customer.

## Setup

```bash
pip install -r {baseDir}/requirements.txt
export OPENAI_API_KEY="your-api-key"
python3 {baseDir}/scripts/wacli.py login <your-wacli-token>
```

Generated files default to `./generated`. Override with
`CONTENT_CREATOR_OUTPUT_DIR`.

## Run

Note: Image generation and transcription can exceed common exec timeouts.
When invoking via OpenClaw's exec tool, set a higher timeout (e.g. 300s).

```bash
# Process all unread requests end to end
python3 {baseDir}/scripts/workflow.py process-all

# Individual tools
python3 {baseDir}/scripts/transcribe.py path/to/request.mp3
python3 {baseDir}/scripts/generate_images.py "A cute cat wearing a hat"
python3 {baseDir}/scripts/generate_images.py prompts.txt   # one prompt per line
python3 {baseDir}/scripts/wacli.py list
```

## Notes

- All scripts raise typed errors (`TranscriptionError`, `ImageGenerationError`)
  and catch specific exceptions, so a single bad request never crashes a batch.
- Network downloads use timeouts and `raise_for_status()`.
- `wacli.py` ships with mock messages; replace `list_messages` / `send_message`
  with calls to your real WhatsApp provider before production use.
