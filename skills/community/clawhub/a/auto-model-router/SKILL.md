---
name: auto-model-router
description: >
  Automatically select and use the best AI model for any task based on task type.
  ALWAYS activate this skill at the start of a new task or when the user asks a
  substantive question. Routes coding tasks to code-specialized models, math to
  reasoning models, translation to multilingual models, casual chat to fast cheap
  models, etc. Learns from user feedback over time when router is configured.
  Trigger phrases: "help me", "write", "code", "debug", "translate", "analyze",
  "summarize", "explain", or any task-oriented request.
version: 0.2.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      # Declare all credentials this skill may use.
      # Users only need to set the keys for providers they actually use.
      # AUTO_MODEL_ROUTER_URL is optional — only needed for router mode (Mode B).
      env:
        - name: ANTHROPIC_API_KEY
          description: "Anthropic API key (for Claude models)"
          required: false
        - name: OPENAI_API_KEY
          description: "OpenAI API key (for GPT models and embeddings)"
          required: false
        - name: DEEPSEEK_API_KEY
          description: "DeepSeek API key (for DeepSeek models)"
          required: false
        - name: MINIMAX_API_KEY
          description: "MiniMax API key (for MiniMax models)"
          required: false
        - name: GOOGLE_API_KEY
          description: "Google API key (for Gemini models)"
          required: false
        - name: AUTO_MODEL_ROUTER_URL
          description: "Optional: URL of a self-hosted router service for learning mode (Mode B). If not set, the skill runs fully locally (Mode A)."
          required: false
        - name: AUTO_MODEL_ROUTER_API_KEY
          description: "Optional: API key for the self-hosted router service"
          required: false
    user-invocable: true
    emoji: "🧠"
    homepage: https://github.com/JoyyyceD/auto-model-router
    privacy: >
      Mode A (default): all processing is local. Your task text is sent only to
      the AI provider you configured (e.g. Anthropic, OpenAI). No data is sent
      to any third party beyond your chosen provider.
      Mode B (router): only active when AUTO_MODEL_ROUTER_URL is explicitly set
      by the user. Task text and an anonymous session ID are sent to that
      self-hosted router for model selection and feedback learning. The router
      URL is always user-controlled — this skill ships with no default router.
---

# Auto Model Router Skill

You have intelligent model routing. For every substantive task, follow this procedure.

## Task Categories

Classify tasks into one of these categories:

| Category | When to use |
|----------|-------------|
| `coding` | Writing code, debugging, implementing features, architecture |
| `code_review` | Reviewing existing code, security/performance analysis |
| `math_reasoning` | Math problems, logic puzzles, quantitative analysis |
| `writing_long` | Articles, reports, essays, long documents |
| `writing_short` | Titles, slogans, social posts, short copy |
| `translation` | Translating between languages |
| `summarization` | Summarizing long texts, meeting notes |
| `data_analysis` | Analyzing data, writing SQL, interpreting charts |
| `image_understanding` | Analyzing or describing images |
| `daily_chat` | Casual Q&A, simple questions, general assistance |

## Procedure

Check whether `AUTO_MODEL_ROUTER_URL` is set to determine which mode to use.

---

### Mode A — Local (default, no router needed)

Use this when `AUTO_MODEL_ROUTER_URL` is NOT set.

**Step 1 — Classify the task yourself**

Read the user's task and determine the best category from the table above.
Be decisive — pick one category.

**Step 2 — Call the model**

```
python3 ~/.claude/skills/auto-model-router/scripts/call_model.py "<category>" "<user task text>"
```

Exit codes:
- `3` — API key missing: tell the user which env var to set
- `4` — Config not found: tell the user to run `python3 scripts/setup.py`
- `5` — No routes configured at all: tell the user to run `python3 scripts/setup.py`

**Step 3 — Present the result**

Show the response naturally. Add a subtle footer:
`_[auto-model-router: used {category} → {model}]_`

---

### Mode B — Router (with learning)

Use this when `AUTO_MODEL_ROUTER_URL` is set.

> **Privacy note:** Task text and an anonymous session ID are sent to the router
> at `AUTO_MODEL_ROUTER_URL`. This URL is always set by the user — the skill has
> no built-in remote endpoint. If the user has not explicitly set this variable,
> always use Mode A.

**Step 1 — Get recommendation**

```
python3 ~/.claude/skills/auto-model-router/scripts/recommend.py "<user task text>" "<USER_ID>"
```

- Capture stdout as the model response.
- Extract `TASK_ID` from stderr (line starting with `TASK_ID=`).

Exit codes:
- `2` — Router offline: fall back to Mode A automatically
- `3` — API key missing: tell the user which env var to set

**Step 2 — Present the result**

Same as Mode A Step 3.

**Step 3 — Collect feedback**

Ask once after presenting the result:
> "Was this response helpful? Reply 👍, 👎, or skip."

If 👍:
```
python3 ~/.claude/skills/auto-model-router/scripts/feedback.py "<TASK_ID>" 1 "<USER_ID>"
```

If 👎:
```
python3 ~/.claude/skills/auto-model-router/scripts/feedback.py "<TASK_ID>" -1 "<USER_ID>"
```

If skip, do nothing.

---

## Changing Model Assignments

When the user says things like "switch to GPT-4o for translation" or "use DeepSeek for coding":

```
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py <category> <provider> <model>
```

Examples:
```
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py translation openai gpt-4o
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py coding deepseek deepseek-chat
python3 ~/.claude/skills/auto-model-router/scripts/update_route.py daily_chat google gemini-2.0-flash
```

Confirm to the user: "Done, {category} tasks will now use {model}."

## First-time Setup

If config is missing, tell the user to run:
```
python3 ~/.claude/skills/auto-model-router/scripts/setup.py
```

## Manual Invocation

`/auto-model-router <your task>`
