---
name: fastrouter-setup
description: "Add the FastRouter AI provider to OpenClaw with all available text and vision models, fetched live from the FastRouter API. Use when: (1) a user wants to set up FastRouter as a model provider, (2) a user says 'set up fastrouter', 'add fastrouter provider', or 'configure fastrouter' along with an API key, (3) a user wants to refresh/update their FastRouter model list. Triggers on phrases like 'set up fastrouter with API key sk-v1-xxxxx', 'add fastrouter provider', 'configure fastrouter', or 'update fastrouter models'."
---

# FastRouter Setup

Add the FastRouter AI provider to OpenClaw with all available text and vision models using only built-in tools (no script execution required).

## Inputs

- **API Key** (required): Starts with `sk-v1-` followed by a hex string. If not provided, ask for it.
- **Base URL** (optional): Defaults to `https://api.fastrouter.ai`

## Steps

### 1. Extract the API key

Parse the API key from the user's message. It starts with `sk-v1-`.

If no API key is found, ask the user for it. Do NOT proceed without one.

### 2. Fetch models

Use `web_fetch` to get the model list:

```
web_fetch url="https://api.fastrouter.ai/v1/models" extractMode="text"
```

### 3. Filter models

From the response JSON, keep only models where:
- `is_active` is true
- `architecture.output_modalities` includes "text"
- `architecture.input_modalities` includes "text" or "image"

For each qualifying model, extract:
- `id` — the model identifier
- `context_length` — context window size
- `top_provider.max_completion_tokens` — max output tokens (if 0 or missing, use min(context_length, 8192))
- Input types: list of "text" and/or "image" from input_modalities

### 4. Build provider config

Construct the provider object (do NOT include a "name" key — OpenClaw rejects it):

```json
{
  "baseUrl": "https://api.fastrouter.ai",
  "api": "openai-completions",
  "apiKey": "THE_API_KEY",
  "models": [
    {
      "id": "model/id",
      "name": "Display Name",
      "contextWindow": 128000,
      "maxTokens": 8192,
      "input": ["text", "image"],
      "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
      "reasoning": false
    }
  ]
}
```

### 5. Update openclaw.json

Use `read` to load `~/.openclaw/openclaw.json`.

Merge the provider into `models.providers.fastrouter`, preserving all other config.

Also add model references to `agents.defaults.models` — for each model, add:
```
"fastrouter/MODEL_ID": {}
```

Use `write` to save the updated config.

### 6. Restart gateway

```bash
openclaw gateway restart
```

This is the only step requiring user approval.

### 7. Report to user

Tell the user:
- How many models were added
- They can switch models with `/model fastrouter/MODEL_ID`
- Suggest popular models (claude, gpt, gemini, deepseek variants)

## Error Handling

- **API unreachable**: Tell the user the FastRouter API may be down, try again later
- **No qualifying models**: Warn that no text/image models were found
- **Config file missing**: Create the full structure from scratch
- **Invalid API key format**: Ask the user to double-check their key

## Notes

- Provider key is `fastrouter`
- Existing fastrouter config will be replaced with fresh model list
- All other providers and settings are preserved
- Cost is set to zero (FastRouter handles billing separately)
- Video-only and audio-only models are excluded
