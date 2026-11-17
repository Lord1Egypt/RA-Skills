---
name: empiriolabs-search
description: Search the web with EmpirioLabs AI and get current results, one answer with its sources, or a research report with citations. Use when the user asks to look something up online, to find recent news, documentation, or sources, to answer a question with citations, or to research a topic in depth. Runs a bundled Python script that picks a search model from the live catalog (or the one you name) and prints the results or saves them to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Search the web with EmpirioLabs AI
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
      - web-search
      - research
      - empiriolabs
    related_skills:
      - empiriolabs-ocr
      - empiriolabs-models
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI web search

Search the web with the [EmpirioLabs AI](https://empiriolabs.ai) search API. The bundled script has three modes: search results, one answer with its sources, and a research report with citations.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Search

```bash
python3 scripts/search.py "latest stable release of Python"
```

Prints a numbered list of results, each with its title, URL, and a short extract:

```text
1. Title of the first result
   https://example.com/first-result
   The opening lines of the page, shortened ...
```

## Answer a question with sources

```bash
python3 scripts/search.py "who maintains the Model Context Protocol" --answer
```

Prints the answer, then the numbered sources it cites.

## Research a topic

```bash
python3 scripts/search.py "state of solid-state batteries in 2026" --research --out ./battery-report.md
```

A research report reads many sources and can take several minutes. It costs more than a search, so confirm it with the user first. With `--out`, the script saves the report and prints a JSON summary:

```json
{
  "model": "MODEL_ID",
  "file": "/home/me/project/battery-report.md",
  "sources": 24,
  "characters": 9120
}
```

## Options

| Option | Meaning |
|---|---|
| `--answer` | Return one answer with its sources. |
| `--research` | Run a research report with citations. |
| `--model ID` | Use a specific model. |
| `--param key=value` | Any other model parameter, for example `--param num_results=5`. |
| `--out PATH` | Save the output (with `.json`, the full result). |
| `--json` | Print the full result as JSON. |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

Search is billed per request, and the price depends on the model and the mode. Check before a run:

```bash
python3 scripts/search.py --list-models
python3 scripts/search.py --list-models --research
```

`*` marks the model used when `--model` is omitted. For a model's parameters, such as result count, date range, or domains to include, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.
