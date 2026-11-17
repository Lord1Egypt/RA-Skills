---
name: empiriolabs-models
description: Find the right EmpirioLabs AI model for a task and look up its price, parameters, limits, and supported endpoints in the live public catalog. Use when the user asks which model to use for text, image, video, audio, transcription, research, embeddings, or 3D, what a model costs, which models support a feature or endpoint, or what parameters a model accepts. No API key needed.
license: MIT-0
compatibility: Requires Python 3.8 or later and network access to api.empiriolabs.ai. No API key is needed because the catalog is public.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Find EmpirioLabs AI models and prices
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://empiriolabs.ai/models
  hermes:
    tags:
      - model-catalog
      - pricing
      - empiriolabs
    related_skills:
      - empiriolabs-image
      - empiriolabs-video
      - empiriolabs-speech
      - empiriolabs-transcribe
---

# EmpirioLabs AI model catalog

Search the live [EmpirioLabs AI](https://empiriolabs.ai) model catalog and read each model's price, parameters, and limits. The catalog is public, so no API key is needed. Prices are the final per-request prices billed to an EmpirioLabs AI account.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`. Python 3.8 or later, nothing to install.

## Find candidates

```bash
python3 scripts/models.py --category image                 # every image model with its price
python3 scripts/models.py --endpoint audio/transcriptions  # models that serve an endpoint
python3 scripts/models.py --search "reasoning" --category text
python3 scripts/models.py --feature image_editing --featured
python3 scripts/models.py --categories                     # category slugs and counts
```

Each row shows the model id, its category, and its price. `*` marks featured models. Add `--json` for machine-readable output and `--limit 0` to show every match.

## Inspect one model

```bash
python3 scripts/models.py --show flux-2-klein-4b
python3 scripts/models.py --show whisper-large-v3-turbo --json
```

`--show` prints the description, supported endpoints, input and output types, features, every price row, every parameter (type, default, options, range), usage notes, and links to the model's docs and Playground page.

## How to recommend a model

1. Narrow by category or endpoint for the task (for example `--category video`).
2. Compare prices in the same unit (per image, per second, per 1M tokens, per minute of audio).
3. Run `--show` on the top choices to check limits that matter: maximum duration or resolution, text length, accepted inputs.
4. Give the user the model id, the price that applies to their request, and any limit that affects it. Pass the id to the other EmpirioLabs AI skills with `--model`.

Categories in the catalog: `text`, `image`, `video`, `audio` (speech and music), `transcription`, `research`, `3d`, `embedding`, `reranker`, `tools`, and `decision`. Common words such as `tts`, `stt`, or `chat` also work with `--category`.

## Related skills

- `empiriolabs-image`, `empiriolabs-video`, `empiriolabs-speech`, and `empiriolabs-transcribe` run the models found here. Each also has `--list-models` for its own endpoint.
- Text models are called through the OpenAI-compatible `POST https://api.empiriolabs.ai/v1/chat/completions` endpoint with an API key from https://platform.empiriolabs.ai/dashboard/api-keys.

Browse the same catalog on the web at https://empiriolabs.ai/models and see the pricing page at https://empiriolabs.ai/pricing. API reference: https://docs.empiriolabs.ai.
