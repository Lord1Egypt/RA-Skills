---
name: context-near-overflow
description: Context window is near capacity, causing the model to drop earlier content silently and produce degraded, partial, or inconsistent output.
emoji: 📉
metadata:
  clawdis:
    os: [macos, linux, windows]
---

# context-near-overflow

When a conversation or task grows large enough to fill the context window, the model begins silently dropping earlier content. The output doesn't error — it degrades. The model appears to be working but is operating on a truncated view of the task, producing answers that are incomplete, inconsistent, or contradictory to earlier parts of the session.

## Symptoms

- Output contradicts or ignores instructions given earlier in the session.
- A multi-part task is completed correctly up to a point, then the later parts are vague, generic, or wrong.
- The model refers to "earlier in our conversation" but misremembers or omits what was said.
- A long document passed as input is summarized or acted on as if the end of it was never read.
- Retrying the same prompt with a fresh session produces noticeably better output.

## What to do

- Split the task. Identify the minimal context that the current step actually needs and discard the rest. Re-inject only what is relevant.
- Summarize and compress. Replace long prior output that is no longer being modified with a compact summary. The summary costs far fewer tokens than the original.
- Use a fresh session per task. Carry in only the outputs of the prior step, not the entire session history.
- Move stable reference material (schemas, instructions, policies) into the system prompt if the host supports it, so user-turn context is reserved for dynamic content.
- If the task genuinely requires more context than the model supports, decompose it into stages: each stage reads the output of the previous one rather than everything accumulated so far.
