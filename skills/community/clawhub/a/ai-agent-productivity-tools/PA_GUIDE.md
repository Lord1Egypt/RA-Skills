# Personal Assistant Build Guide

A practitioner's guide to building effective personal assistant agents using pa-pack.

## Table of Contents

1. [Start Here](#start-here)
2. [Choosing Components](#choosing-components)
3. [Customizing Prompts](#customizing-prompts)
4. [Evaluating Quality](#evaluating-quality)
5. [Common Pitfalls](#common-pitfalls)
6. [Advanced: Context Kernel](#advanced-context-kernel)

## Start Here

Don't turn on everything at once. Start with **one** component:

- If you get a lot of email → **Triager**
- If you struggle with drafting → **Drafter**
- If you miss meetings or double-book → **Scheduler**
- If you forget follow-ups → **Follow-Up**

Run it for a week. Tune the prompts. Then add a second component.

## Choosing Components

### Triager Setup

1. Define your priority matrix (what makes something urgent vs important)
2. Provide sample messages so the scoring aligns with your judgment
3. Set thresholds: what score triggers "reply now" vs "reply later"

### Drafter Setup

1. Pick a default tone (most people start with concise)
2. Collect 5-10 examples of your own writing in that tone
3. Paste them into the prompt as few-shot examples
4. Iterate until drafts sound like you

### Scheduler Setup

1. Connect your calendar API (read-only is enough)
2. Define buffer rules (e.g., no back-to-back meetings without 15m gap)
3. Set working hours
4. Test with 10 real scheduling requests

### Follow-Up Setup

1. Define your reminder cadence (e.g., 3 days before, 1 day before, day of)
2. Set an escalation path (who gets pinged if you miss it)
3. Use a simple storage: file, note app, or database

## Customizing Prompts

Prompts live in `scripts/prompts/`. Override them in `custom-prompts/`.

Rules for good prompts:

- **Be specific:** "Write a concise email" is weak. "Write a 2-3 sentence email that states the decision, gives one reason, and names the next step" is strong.
- **Provide examples:** Few-shot examples are the single biggest quality lever.
- **Set boundaries:** "Do not apologize if it was not your fault." "Do not ask rhetorical questions."
- **Define the audience:** "The reader is a busy VP. They scan, they don't read."

## Evaluating Quality

Measure, don't guess:

| Metric | How to Measure | Target |
|--------|--------------|--------|
| Draft acceptance rate | % of drafts you send unedited | >70% |
| Triage accuracy | % of triage suggestions you agree with | >80% |
| Scheduling conflicts | % of scheduled meetings that conflict | <5% |
| Follow-up misses | % of tracked items you miss | <10% |

Review weekly. Adjust prompts when metrics slip.

## Common Pitfalls

1. **Over-automation:** Automating too fast leads to embarrassing mistakes. Start with suggestions.
2. **Under-context:** The drafter is only as good as the thread history you give it.
3. **Ignoring edge cases:** What happens on holidays? When you're OOO? When the recipient is in a different timezone?
4. **Prompt drift:** If you edit prompts frequently without versioning, you lose reproducibility.
5. **Expecting mind-reading:** The PA does not know your unspoken preferences. Document them.

## Advanced: Context Kernel

The context kernel is a lightweight session store. It holds:

- Recent decisions (so the PA remembers what you chose last time)
- Active projects (so references like "the Berlin deal" resolve)
- Preferences that change by context (formal for clients, casual for team)

Implementation is left to the practitioner. Simplest: append to a JSONL file.

```python
# Example: simple context kernel append
import json, datetime

def log_context(action, details):
    with open("context.jsonl", "a") as f:
        f.write(json.dumps({
            "ts": datetime.datetime.now().isoformat(),
            "action": action,
            "details": details
        }) + "\n")
```

## Support

- Issues: https://github.com/certainlogic/pa-pack/issues
- Discussions: https://github.com/certainlogic/pa-pack/discussions
