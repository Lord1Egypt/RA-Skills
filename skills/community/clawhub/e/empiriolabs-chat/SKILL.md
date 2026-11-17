---
name: empiriolabs-chat
description: Ask an EmpirioLabs AI text model a question and get its answer. Use when the user asks for a second opinion from another model on code, a plan, or a draft, wants a specific EmpirioLabs AI model to answer, wants several models to answer the same prompt side by side, or needs a model that reads images to describe a picture. Runs a bundled Python script that picks a text model from the live catalog (or the ones you name), can attach text files and images to the prompt, and prints the answer or saves it to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Ask EmpirioLabs AI text models
  openclaw:
    primaryEnv: EMPIRIOLABS_API_KEY
    requires:
      env:
        - EMPIRIOLABS_API_KEY
      anyBins:
        - python3
        - python
    envVars:
      - name: EMPIRIOLABS_API_KEY
        required: true
        description: "EmpirioLabs AI API key (starts with sk-empiriolabs-). Create one at https://platform.empiriolabs.ai/dashboard/api-keys"
    homepage: https://empiriolabs.ai
  hermes:
    tags:
      - chat
      - second-opinion
      - empiriolabs
    related_skills:
      - empiriolabs-models
      - empiriolabs-search
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI chat

Ask a text model on [EmpirioLabs AI](https://empiriolabs.ai) a question and read its answer. The bundled script sends one prompt, with optional instructions, text files, and images, to one model or to several.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Ask a question

```bash
python3 scripts/chat.py "Explain the tradeoffs between optimistic and pessimistic locking"
```

Prints the answer as text. The model and its token counts go to standard error, so the answer can be piped or captured on its own.

## Get a second opinion on a file

```bash
python3 scripts/chat.py "Review this function for bugs and edge cases" --file ./src/parser.py
python3 scripts/chat.py "Does this plan miss a step?" --file ./PLAN.md --system "You are a careful reviewer. Be specific."
git diff | python3 scripts/chat.py - --system "Review this diff for bugs."
```

`--file` attaches a UTF-8 text file under its file name and can be repeated (1 MB in total). `--system` sets the instructions the model follows. A prompt of `-` is read from standard input.

Everything attached is sent to the model, so attach only what the user agreed to share.

## Ask about an image

```bash
python3 scripts/chat.py "What does this screenshot show?" --image ./screenshot.png
python3 scripts/chat.py "Compare these two charts" --image https://example.com/a.png --image ./b.png
```

`--image` takes an https URL or a local file of up to 20 MB. Without `--model`, a model that reads images is chosen. A named model that does not read images is refused before anything is sent.

## Have several models answer

```bash
python3 scripts/chat.py "Which design is simpler to operate, and why?" --model MODEL_A --model MODEL_B
```

Each model answers the same prompt, and each answer is printed under a heading with the model id:

```text
## MODEL_A

The first model's answer ...

## MODEL_B

The second model's answer ...
```

Each model is billed for its own request. If one model fails, the others still answer and the script exits with `1`.

## Save the answer

```bash
python3 scripts/chat.py "Summarize these notes in five bullet points" --file ./notes.md --out ./summary.md
```

With `--out`, the script saves the answer and prints a JSON summary:

```json
{
  "model": "MODEL_ID",
  "file": "/home/me/project/summary.md",
  "characters": 640
}
```

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model. Repeat it to ask several models. |
| `--system TEXT` | Instructions the model follows for this request. |
| `--file PATH` | Attach a text file to the prompt. Repeatable. |
| `--image URL_OR_PATH` | Attach an image for a model that reads images. Repeatable. |
| `--max-tokens N` | Upper limit on the length of the answer, in tokens. |
| `--temperature X` | Sampling temperature. |
| `--param key=value` | Any other model parameter, for example `--param reasoning_effort=high`. |
| `--out PATH` | Save the answer (with `.json`, the full result). |
| `--json` | Print the full result as JSON. |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

A request is billed at the model's listed price, which is per token for a text model. Check before a run:

```bash
python3 scripts/chat.py --list-models
python3 scripts/chat.py --list-models --vision
```

`--vision` lists only the models that read images. `*` marks the model used when `--model` is omitted. For a model's context window, parameters, and limits, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` a request failed or a model returned no text (the message says why), `2` invalid arguments.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.
- "The model returned no text (finish reason: length)": the answer was cut off before it began. Raise `--max-tokens`.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.
