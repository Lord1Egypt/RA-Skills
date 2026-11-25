# Dataset Format and Preparation

Applies to Serverless Fine-Tuning training and validation files. Source:
docs.crusoe.ai `serverless-fine-tuning/fine-tune-a-model` (verified 2026-11-18).

## Hard constraints

- **Format**: a single `.jsonl` or `.parquet` file, **3 GB or smaller**.
- **Schema**: every row is a JSON object with a `messages` array of chat turns:
  `{"role": "system"|"user"|"assistant", "content": "..."}`.
- **Loss masking**: loss is computed on **assistant turns only**; every other
  role is masked. Whatever the model must learn to *produce* belongs in
  assistant turns.
- **Validation split**: if no `validation_file` is given to the job, Crusoe
  automatically holds out 10% of the training data.
- **Reasoning**: single-turn reasoning and multi-turn non-reasoning work;
  **multi-turn reasoning is not supported yet**.

## Workflow

1. Get or build the user's data as JSONL chat rows.
2. Run the validator (from this skill's root):

   ```bash
   python3 scripts/validate_dataset.py <train.jsonl> [--model <base-model-id>]
   ```

   It reports errors (will fail the job), warnings (quality/model-fit), and
   stats (rows, role balance, length distribution, duplicate rows). Fix
   errors before uploading; discuss warnings with the user.
3. If the user's data isn't already in chat format (CSV, documents,
   prompt/completion pairs), convert it: put the *input* in `user` turn(s) and
   the *target output* verbatim in the `assistant` turn. Preserve exact
   output formatting — the model learns whatever the assistant turns contain,
   including trailing whitespace patterns and JSON formatting.
4. Optionally carve out a validation file with
   `python3 scripts/validate_dataset.py train.jsonl --holdout 0.1 --val-out val.jsonl`
   (deterministic, seeded split). A held-out validation set gives cleaner loss
   curves than the automatic 10% split.
5. Show the user a sample row and the row count before uploading.

## Model-specific quirks

Some base models have pretrained formatting habits that the dataset must
respect. Apply the rule matching the chosen base model:

| Base model | Rule |
|---|---|
| `gpt-oss-*` | gpt-oss is pretrained to emit `analysis` before `final`. If the dataset only trains on final content, add an empty `"thinking": ""` field to each assistant turn: `{"role": "assistant", "content": "...", "thinking": ""}`. |
| `meta-llama/Llama-3.1-8B-Instruct`, `Llama-3.3-70B-Instruct` | An assistant turn containing both a tool call and content renders **only the tool call** (content is dropped). Don't train it to emit both; keep them in separate turns. |
| Thinking models (Qwen3.5, GLM-5.x) | If the dataset has no thinking content, the fine-tuned model tends to emit its answer into the reasoning channel: at inference `content` comes back `null` with the answer in `message.reasoning`. Mitigate by passing `"chat_template_kwargs": {"enable_thinking": false}` at inference (verified live), or by training with thinking-formatted turns (e.g. empty `"thinking": ""` field, as with gpt-oss). |
| `google/gemma-4-31b-it` | An assistant turn with both a tool call and content renders **content before the tool call**, which reads unnaturally. To get content *after* a tool call, put it in a separate assistant turn following the tool call. |

The validator emits these warnings automatically when `--model` is passed.

## Tool calls

Assistant tool calls use the standard shape; `function.arguments` must be a
JSON-encoded **string**, not an object:

```json
{
  "role": "assistant",
  "content": "",
  "tool_calls": [
    {
      "id": "call_1",
      "type": "function",
      "function": {"name": "get_weather", "arguments": "{\"city\": \"SF\"}"}
    }
  ]
}
```

`tool` role turns carry the tool result back. Keep the tool-call/tool-result
ordering you want the model to reproduce at inference.

## Length limits

Rows exceeding the base model's maximum sequence length fail the job by
default (`overlong_row_behavior: "error"`). The validator estimates row
token counts and flags rows over the model's context window. Options:

- Trim or split long rows in the data (preferred), or
- set `overlong_row_behavior: "drop"` on the job to silently skip overlong
  rows (loses data; know what's being dropped).

## Common failure patterns to check by eye

- Multiple different system prompts across rows — fine technically, but
  usually a sign of mixed sources; confirm intent with the user.
- Assistant turns that are empty and have no tool calls — wasted training
  signal or a conversion bug.
- Wide role imbalance (e.g. no system turn at all when the task expects one).
- Data leakage of the answer into the user/system turns.
