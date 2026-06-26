---
name: visibility-monitor
description: >
  Use when the user wants to run or design AI visibility monitoring for a developer tool, API, SDK, or open-source project. Covers Query Pool execution, evidence logging, four-metric scoring, weekly reporting, anomaly detection, and action prioritization across multiple LLMs and languages.
allowed-tools: Read, Write, Edit, Bash
metadata:
  openclaw:
    author: "veeicwgy"
    homepage: "https://github.com/veeicwgy/devtool-answer-monitor"
    requires:
      env:
        - OPENAI_API_KEY
        - OPENAI_BASE_URL
      bins:
        - python3
        - bash
    primaryEnv: OPENAI_API_KEY
    env:
      - name: OPENAI_API_KEY
        description: "Optional provider API key for API collection mode. Not needed for quickstart replay or manual paste mode."
        required: false
        sensitive: true
      - name: OPENAI_BASE_URL
        description: "Optional OpenAI-compatible gateway URL for multi-provider monitoring."
        required: false
        sensitive: false
---

# visibility-monitor

Use this skill to turn repeated model checks into a consistent visibility monitoring workflow.

## Safety

- Use `quickstart replay` or `manual paste mode` first when the user does not need live API calls.
- Keep provider keys in local shell environment variables. Do not ask users to paste secrets into chat.
- Inspect `install.sh`, `quickstart.sh`, and the selected runner before executing Bash commands.

## Trigger

Use this skill when the user already has, or is ready to create, a Query Pool and wants to know:

1. whether the product is being mentioned;
2. whether mentions are positive, neutral, or negative;
3. whether the model understands the product's capabilities;
4. whether the model understands the product's ecosystem and integrations.

## Quick Start

### Zero-key paths first

- `bash quickstart.sh` replays sample data and does not require provider keys.
- `python -m devtool_answer_monitor run --manual-responses ...` scores copied answers without live API calls.

### Choose the right runner

| Runner | API Type | Works with | Use when |
|---|---|---|---|
| `scripts/run_monitor.py` | Responses API | OpenAI models only | GPT-4o, GPT-4.1 and variants |
| `scripts/run_chat_completions.py` | Chat Completions API | Any OpenAI-compatible provider | Claude, Gemini, DeepSeek, Qwen, MiniMax, GLM, or any gateway |

**For multi-model coverage across providers, always use `run_chat_completions.py`.**

```bash
python scripts/run_chat_completions.py \
    --query-pool data/query-pools/mineru-example.json \
    --model-config data/models.sample.json \
    --out-dir data/runs/my-run
```

Before running the command above, verify that `OPENAI_API_KEY` is configured in the local shell. `OPENAI_BASE_URL` is optional and only needed for gateways or proxies.

Then annotate scores and generate the report:

```bash
python -m devtool_answer_monitor report \
    --input data/runs/my-run/raw_responses.jsonl \
    --output-dir data/runs/my-run
```

## Outputs

| Output | Description |
|---|---|
| Monitoring summary | overall run snapshot |
| Four-metric score table | mention, positive mention, capability, ecosystem |
| Anomaly list | urgent issues by model and query |
| Action backlog | next content, repair, and verification moves |

## Next Best Skill

If the main issue is missing or weak content, use `visibility-content-check`.

If the main issue is negative or wrong answers, use `visibility-repair`.
