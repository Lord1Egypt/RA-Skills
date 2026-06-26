---
name: ask-more
description: Multi-LLM consultation for complex questions. Trigger when user sends "/ask [question]", "/ask" (no args, consult on recent conversation), "/ask --preset NAME [question]", or "/ask --compare [question]" (raw side-by-side, no synthesis). Spawns parallel subagents with different models, collects answers, extracts consensus/differences/conflicts, returns structured diff report with actionable synthesis. Use for second opinions, blind spot detection, and decision support.
---

# Ask-More

Consult multiple LLMs in parallel, then merge answers into a structured diff report: consensus, unique insights, conflicts, and actionable next steps.

## Configuration

Config file: `skills/ask-more/config.yaml`

If missing, copy from `skills/ask-more/config.example.yaml` and guide user through setup (see § First-Use Setup).

### Required
- `models` — list of model IDs (≥2), must be providers configured in the gateway

### Optional
- `presets` — named model groups (see § Presets)
- `synthesis_model` — separate model for diff merge (must NOT be in the models pool)
- `enable_logging` — log run results to `logs/runs.jsonl`

### Validation
Run `bash skills/ask-more/scripts/load-config.sh skills/ask-more` to validate config. It uses proper YAML parsing and checks: model count, preset validity, synthesis_model conflicts.

### First-Use Setup
When `/ask` is triggered but no models configured:
1. List providers already in the gateway
2. Suggest 2-3 diverse models from different providers
3. Offer to write config.yaml for them
4. Do NOT block — get them running in one interaction

## Commands

| Command | Description |
|---------|-------------|
| `/ask [question]` | Consult all configured models |
| `/ask` | Consult on the most recent conversation topic |
| `/ask --preset <name> [question]` | Use a named preset model group |
| `/ask --compare [question]` | Raw compare mode: show responses side-by-side, no synthesis |

## Presets

If `presets` is configured in config.yaml, users can select a named group:

```yaml
presets:
  fast:
    - google/gemini-2.5-flash
    - deepseek/deepseek-chat
  deep:
    - anthropic/claude-opus-4
    - openai/gpt-4o
    - google/gemini-2.5-pro
```

When `--preset <name>` is used, override the default `models` with the preset's list for that run. If the preset doesn't exist, list available presets and abort.

## Workflow

### 1. Parse trigger

- `/ask <question>` → use the provided question
- `/ask` (no args) → use the most recent user question/topic from conversation. **If the recent topic is ambiguous, ask the user to clarify instead of guessing.**
- `/ask --preset <name> ...` → use preset model group
- `/ask --compare ...` → raw compare mode (skip step 6, go directly to step 7b)

**Pre-flight check:** If the question is trivially simple or empty (e.g., `/ask hi`, `/ask ok`), warn the user that multi-model consultation may not add value for this type of question, and confirm they want to proceed.

### 2. Privacy check (first use only)

Read config. If `privacy_acknowledged` is `false`:

> ⚠️ **隐私提示：** ask-more 会将问题摘要发送给您配置的多个模型 provider（如 OpenAI、Google、Anthropic 等）。请勿在涉及高度敏感信息的场景使用。
>
> 继续使用即表示您已知悉。

Set `privacy_acknowledged: true` in config and proceed.

### 3. Model availability pre-check

Before context packing, verify that configured models are likely reachable:
- Check that each model ID exists in the gateway's provider config
- If any model is not found, warn the user and suggest removing it
- If fewer than `min_models` are available, abort early with a clear message

This prevents users from waiting through the full flow only to discover models are misconfigured.

### 4. Context Packing

Rewrite the user's question into a **self-contained description**:

- Summarize relevant background (what was discussed, constraints, requirements)
- Replace all pronouns/references ("this", "that plan") with concrete descriptions
- State the core question explicitly
- **Write neutrally** — do NOT inject the primary model's own opinion or framing
- Explicitly note any assumptions you introduced that weren't in the original conversation

**Summary mode** (default, `context_mode: summary`):
- Distill to 500-1000 words

**Full mode** (`context_mode: full`):
- Include the last N turns of raw conversation verbatim (N = `full_mode_max_turns`)
- Prepend a 2-3 sentence summary of what the conversation is about
- Append the explicit question at the end

### 5. Confirmation (editable)

Present to user:

```
📋 背景：[packed background]
❓ 问题：[explicit question]
⚠️ 假设：[any assumptions introduced by packing, if any]
🤖 将咨询：[model list]
💰 预估：[N] 次模型调用，约 $X.XX（rough estimate based on model pricing tiers）

确认发送？你也可以直接修改上面的问题描述。
请注意检查问题描述是否准确、中立、没有偏向性。
```

Wait for user response:
- Confirm → proceed
- User sends modified text → use their version, re-confirm
- Cancel → abort

**Dedup check:** Hash the packed question. If an identical question was asked in the last 5 minutes, warn user and confirm they want to re-run (saves cost on accidental double-triggers).

### 6. Parallel consultation

For each model, spawn a subagent:

```
sessions_spawn(
  task: <packed question + subagent prompt from references/prompt-templates.md>,
  model: <model-id>,
  mode: "run",
  runTimeoutSeconds: <timeout_seconds>
)
```

**Progress feedback:** After spawning, show status. As each model completes, update:
```
⏳ 已收到 1/3 回复（Claude ✅）...
⏳ 已收到 2/3 回复（Claude ✅ GPT ✅）...
✅ 全部收到，正在合并...
```

**State tracking per model:**
- `pending` → spawned, waiting
- `success` → response received
- `failed` → API error or malformed response
- `timed_out` → exceeded timeout_seconds

After all models complete or time out, call `sessions_yield()` to collect results.

**Failure handling:**
- If a model returns an error → mark as `failed`, log reason
- If a model returns an extremely short response (<50 words) or a refusal → mark as `degenerate`, include in report metadata but exclude from synthesis
- If fewer than `min_models` succeeded (non-degenerate) → inform user, offer to show whatever raw responses are available, abort synthesis

### 7a. Diff merge (normal mode)

Read the merge prompt from `references/prompt-templates.md` § "Diff Merge Prompt".

If `synthesis_model` is configured, use it for this step. **Verify synthesis_model is NOT in the consultation pool** — if it is, warn and fall back to primary model.

**Degenerate response handling in merge prompt:**
- If a model refused to answer, note it as "[Model] declined to answer (safety/policy)"
- If a model gave an extremely short/generic response, note it as "[Model] provided limited input"
- These should appear in the report metadata, not pollute the consensus/diff analysis

**Unanimous agreement shortcut:**
If all models give substantially the same answer with no meaningful unique insights or conflicts, use a shorter output:
```
## 🔍 Ask-More 咨询报告

📝 咨询问题：[question]

✅ 高度一致：所有模型观点基本一致。
本次咨询的增量价值有限，以下是综合要点：
- ...
- ...

🎯 综合判断：...

📊 参与模型：[all models] ✅
```

**Normal output structure:**
```
## 🔍 Ask-More 咨询报告

📝 咨询问题：[question]

🤝 共识观点：（多数模型都提到的）
- ...
⚠️ 共识代表被咨询模型之间的一致看法，不等于客观事实。模型可能共享相同的训练偏差。

💡 差异观点：
- 🟦 [Model A]：...
  假设前提：...
- 🟩 [Model B]：...
  假设前提：...

⚡ 冲突点：（模型之间互相矛盾的）
- [Model A] 认为 X，但 [Model B] 认为 Y
  → 分歧原因：...（不同假设？不同优先级？不同证据？）
  ⚠️ 如涉及高风险决策，请以人工判断为准，不要直接采信任何一方。

🎯 综合判断：
- 当前最佳判断：...
- 不确定性标签：[高一致性 / 假设敏感 / 证据薄弱 / 价值判断分歧]
- 信息缺口：...
- 建议下一步：...

📊 参与模型：[Model A] ✅ | [Model B] ✅ | [Model C] ⏱️超时
```

**Chat interface adaptation:** In Telegram/Discord/WhatsApp, deliver a **3-5 bullet summary first**, then the full report. Avoid wall-of-text.

### 7b. Raw compare mode (`--compare`)

Skip synthesis entirely. Present each model's response in sequence:

```
## 🔍 Ask-More 原始对比

📝 问题：[question]

### 🟦 [Model A]
[full response]

### 🟩 [Model B]
[full response]

### 🟨 [Model C]
[full response]

📊 参与模型：[all] ✅
```

This mode is for users who want to judge themselves without synthesis bias.

### 8. Graceful degradation

When things go wrong, degrade gracefully instead of failing silently:

| Scenario | Action |
|----------|--------|
| Synthesis model fails | Fall back to primary model for merge. If that also fails, return raw responses (like --compare mode) with a note. |
| Only `min_models` barely respond | Proceed but mark report as "⚠️ 低置信度：仅 N 个模型回复" |
| Only 1 model responds | Abort synthesis, show the single response with note: "仅收到 1 个回复，无法进行多模型对比" |
| All models time out | Abort, suggest user check model config and try again |
| Model returns refusal | Exclude from synthesis, note in report as policy difference |
| Model returns gibberish/extremely short | Exclude from synthesis, note as degenerate response |

### 9. Logging

If `enable_logging: true` in config, after each run, log to `skills/ask-more/logs/runs.jsonl`:

```json
{
  "timestamp": "2026-03-25T01:30:00+08:00",
  "question_hash": "sha256_first8",
  "models": ["claude-sonnet-4", "gpt-5.4", "gemini-2.5-pro"],
  "results": [
    {"model": "claude-sonnet-4", "status": "success", "latency_ms": 34000, "response_words": 850},
    {"model": "gpt-5.4", "status": "success", "latency_ms": 44000, "response_words": 1200},
    {"model": "gemini-2.5-pro", "status": "timed_out", "latency_ms": 30000}
  ],
  "synthesis_status": "success",
  "total_time_ms": 48000,
  "mode": "normal"
}
```

Use `bash skills/ask-more/scripts/log-run.sh <skill-dir> '<json>'` to append.

## Prompt Engineering Notes

### Sub-model prompt design
The subagent prompt (in `references/prompt-templates.md`) explicitly:
- Structures output as: assumptions → analysis → risks → recommendations
- **Encourages challenging the question's premises** — don't just answer, check if the question itself has flawed assumptions
- Uses soft word limit (~800 words) without hard truncation

### Context packing discipline
- Write neutrally — no opinion injection
- Explicitly list any assumptions introduced by packing
- User can edit the packed question — this is a core feature, not an afterthought

### Merge prompt discipline
- Sections 1-3 (consensus/diff/conflicts): faithful to model outputs, no added analysis
- Section 4 (synthesis): clearly labeled as synthesis, not truth
- Distinguish true conflicts from mere phrasing differences
- Include uncertainty labels: 高一致性 / 假设敏感 / 证据薄弱 / 价值判断分歧
- Cite which model supports each claim
- Handle degenerate/refusal responses explicitly
- For high-stakes conflicts: escalate with warning instead of resolving

## Extensibility

### Adding new modes
The architecture supports pluggable consultation modes beyond normal and compare:
- **Debate mode** — models critique each other's responses in rounds
- **Red-team mode** — one model defends, others attack
- **Domain-specific merge** — different prompt templates for coding / product / legal / research questions

To add a mode: create a new prompt template in `references/`, add a command flag, and branch in step 7.

### Model metadata (future)
For smarter model selection, config could include per-model metadata:
```yaml
model_meta:
  anthropic/claude-sonnet-4:
    strengths: [reasoning, nuance, safety]
    cost_tier: medium
  openai/gpt-4o:
    strengths: [breadth, speed, coding]
    cost_tier: medium
```
