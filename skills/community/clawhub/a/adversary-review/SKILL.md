---
name: adversary-review
version: 1.2.0
description: "Mandatory adversarial review of all agent outputs. After drafting any response, a second AI instance (sub-agent) reviews and challenges the draft before delivery. Note: this sends draft text to the configured model API."
tags:
  - quality
  - review
  - safety
  - meta
---

# Adversary Review

Every response to the user must pass adversarial review before delivery.

## When to Use

**EVERY response to the user**, without exception. This is a mandatory quality gate.

## How It Works

After drafting your response (but before sending it), spawn a sub-agent with a critical reviewer persona. The sub-agent examines your draft for problems, then you revise based on its feedback.

### Step 1: Draft Your Response

Write your response as you normally would. Do not send it yet.

### Step 2: Spawn Reviewer Sub-Agent

Use `sessions_spawn` with `mode="run"` and a cheaper model (e.g. `qwen3.5-plus`, `gpt-4o-mini`) to minimize cost. The reviewer does not need the full tool suite — it only reads text and outputs critique.

> **Note:** This sends your draft text to the configured model provider's API. If you use cloud-based models, data will be sent to the provider's servers. Check your provider's data policy if handling sensitive content. For truly local review, configure a local model (e.g. ollama, LM Studio).

Spawn with this prompt template:

```
You are an adversarial reviewer. Examine the following draft response critically.

Draft:
"""
[YOUR DRAFT HERE]
"""

Check for:
1. Factual errors or unsubstantiated claims
2. Missing important caveats or edge cases
3. Logical contradictions
4. Tone issues (too apologetic, too confident, dismissive, etc.)
5. Missing follow-up suggestions that would be valuable
6. Overly verbose sections that could be trimmed
7. Any advice that could backfire or cause problems

Respond with exactly one of:
- PASS + one-line reason why it's fine
- List of specific issues, each with:
  - Where the problem is
  - Why it's a problem
  - Suggested fix

Be harsh. Be picky. Better to over-catch than to miss. You are the quality gate.
```

### Step 3: Apply Feedback

- **Sub-agent says PASS** → deliver your draft as-is
- **Sub-agent raises valid points** → revise your draft, then deliver the improved version
- **Sub-agent is clearly wrong** → trust your own judgment, deliver your version

### Step 4: Deliver

When the review leads to substantive changes, briefly note the improvement (e.g. "Review caught X, fixed Y"). For minor edits, no need to mention. Focus on delivering the best result.

## Privacy & Safety

- The draft text is sent to a second AI model instance via the configured model API. If you use cloud-based models (e.g. qwen3.5-plus, gpt-4o-mini), this will send data to the provider's servers. For local-only review, use a local model provider (e.g. ollama, LM Studio).
- Only the draft text (not full conversation history) is shared with the reviewer.
- If the draft contains sensitive data (PII, credentials, etc.), the agent should skip the review step automatically.
- Review exchanges are not persisted beyond the current agent session.

## Exceptions

These situations do NOT need review:
- `HEARTBEAT_OK`
- System-level acks (tool results, NO_REPLY)
- Purely mechanical confirmations with zero opinion content

## Why This Matters

LLM outputs can contain subtle errors, missing context, or tone issues that are easy to miss from the creator's perspective. A second "pair of eyes" that is explicitly adversarial catches problems before they reach the user. This is the agent equivalent of code review.

Note: This review step adds latency and token usage per response.

## Technical Details

No special configuration needed. To disable review, uninstall this skill.
