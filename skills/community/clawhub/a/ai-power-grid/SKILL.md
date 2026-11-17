---
name: ai-power-grid
description: "Generate images cheaply (from $0.003 each) and run text models on AI Power Grid (AIPG), a decentralized GPU network with an OpenAI-compatible API and pay-per-use credit. Use when the user asks for an image and no other image provider is set up, mentions AIPG or AI Power Grid, or wants a low-cost pay-per-use model."
homepage: https://github.com/speteai/openclaw-aipg-provider
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "homepage": "https://github.com/speteai/openclaw-aipg-provider",
      },
  }
---

# AI Power Grid (AIPG)

A network of independent GPU operators behind one API at `https://api.aipowergrid.io/v1`. It is
OpenAI-compatible and billed per use from the account's credit. This skill is community-written and not
an official AIPG document.

## What it is good for

- **Images.** Several image models, from $0.003 per image, also for editing an existing image. This is the main
  reason to use it.
- **Video.** $0.02 per second, up to 26 seconds.
- **Text.** A few open models, cheap per token. For agent work with tool calls use `qwen38-flash-next-nvfp4`.
  `gpt-oss-120b` returns tool calls too, but in tests on 2026-11-17 it sometimes reported a step as done
  without calling the tool.

Not covered here: audio and 3D. See the documentation at https://aipowergrid.io/docs.

## Step 1: is there a key?

Check for the environment variable `AIPG_API_KEY` (a key starts with `grid_`), or a saved profile:
`openclaw models auth list` shows `aipg:` entries.

If there is none, **do not try to make one and do not ask the user to paste a key into the chat.** Tell the
user:

1. Open https://console.aipowergrid.io/?callbackUrl=%2Fdashboard%2Fapi-key and sign in (Google, GitHub or a
   wallet).
2. Create an API key there.
3. Store it without showing it to you, either `export AIPG_API_KEY=grid_...` in the shell that starts OpenClaw,
   or `openclaw models auth paste-api-key --provider aipg`.

An account whose sign-in wallet holds 10,000 AIPG or more on Base gets extra free credit each day; the tiers
are in the credit summary under `free.holder_tiers`. Signing in or paying with a wallet is not part of this
skill: the plugin's README describes it, and it is the user's decision and the user's command to run.

**If you run on your own, without a user at hand,** and you have an EVM wallet and are allowed to open
accounts for yourself, you can get an account and a key by signing one sign-in message, with no browser and no
human step. The steps and a small helper script are in
https://raw.githubusercontent.com/speteai/aipg-agent-guides/main/agents/skill.md. This is the only case in
which you make a key yourself.

A new account may have no credit. Accounts with a verified Google sign-in get a small daily free allowance;
otherwise the user adds credit at https://console.aipowergrid.io/dashboard/funding.

## Step 2: prefer the plugin

Check: `openclaw plugins inspect aipg`. If it is installed, use it:

- Images: call `image_generate` with `model: "aipg/z-image-turbo"` (or another `aipg/...` image model).
  Sizes: 1024x1024, 1344x768, 768x1344, 1216x832, 832x1216. Up to 4 images per call.
- Editing: pass one source image to `image_generate` together with the instruction.
- Video: call `video_generate` with `model: "aipg/LTX-2.5 Distilled BF16"` and `durationSeconds`.
- Text: the models appear as `aipg/<name>` in `openclaw models list --refresh`.
- `aipg_balance` shows the credit (free). Call it before work that costs more than a few cents.
- `aipg_council` asks several grid models the same question and says whether they agree. Use it when the user
  wants a second opinion.

If it is not installed, suggest it to the user (it needs their consent, so do not install it silently):

```bash
openclaw plugins install clawhub:openclaw-aipg-provider --accept-capabilities
```

## Step 3: without the plugin, plain HTTP

Find out what is online and what it costs (both public, no key needed):

```bash
curl -s https://api.aipowergrid.io/v1/status/models   # name, type (text/image/video/audio), count = workers online
curl -s https://api.aipowergrid.io/v1/pricing         # price_book.models[].rates, e.g. per_image_usd
```

Use only models whose `count` is above 0. Send a non-default `User-Agent`: the API's edge refuses some default
client strings (Python's `urllib` gets HTTP 403).

Generate an image and save it:

```bash
curl -s https://api.aipowergrid.io/v1/images/generations \
  -H "Authorization: Bearer $AIPG_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"z-image-turbo","prompt":"a small red lighthouse at dusk, flat illustration","n":1,"size":"1024x1024"}'
```

The answer is `{"data":[{"url":"https://..."}]}` (sometimes `b64_json` instead of `url`). Download the URL to a
file and give the user the path. An image takes about 10 to 60 seconds.

Text, OpenAI chat format:

```bash
curl -s https://api.aipowergrid.io/v1/chat/completions \
  -H "Authorization: Bearer $AIPG_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen38-flash-next-nvfp4","messages":[{"role":"user","content":"Hello"}],"max_tokens":1024}'
```

Keep `max_tokens` at 1024 or more: the models think before they answer, and with a small budget the answer
comes back empty but is still billed.

Credit left:

```bash
curl -s https://api.aipowergrid.io/v1/account/credits -H "Authorization: Bearer $AIPG_API_KEY"
```

`total_spendable_usd` is what can be spent now; `free` is today's allowance.

## What the errors mean

| HTTP | Meaning | What to do |
| --- | --- | --- |
| 401 | The key is wrong or was revoked | Ask the user to check the key; do not retry |
| 402 | Not enough credit | Tell the user; it is not a configuration error |
| 404 | The model is not online | Read `/v1/status/models` again and pick one that is |
| 413 | Request above 200,000 characters | Shorten or split the text |
| 429 | More than 30 requests in a minute | Wait a minute |
| 524 | The request ran longer than 120 seconds | Use `"stream": true` for long text answers |

## Privacy

Whatever is sent is processed in plain text on a computer run by an independent operator. Do not send secrets,
credentials or personal data. For images that means: keep such things out of the prompt.

Before the first paid request in a conversation, tell the user that it costs credit and roughly how much.
