---
name: agent-verifier
description: Pre-send verification for outbound agents — a small, separate guardian you put in front of send() so every message (email, social, helpdesk reply) gets an independent verdict across deterministic gates (calendar, redlist, regex) plus an optional LLM semantic check, with a per-message audit log a regulator can read.
version: 0.2.0
homepage: https://workloft.ai/labs/notes/pre-send-verifier-2026-05-09.html
metadata:
  openclaw:
    emoji: "🛂"
    requires:
      bins:
        - python3
---

# agent-verifier

When an agent speaks for the firm, "the model was careful" is not a control. The
producer model that drafts the message cannot also be the control that approves
it. `agent-verifier` is the small, separate guardian you put in front of `send()`
so every outbound has an independent verdict — and a per-message log a regulator
can read. Python 3.10+ standard library only; bring your own LLM.

The library lives at `{baseDir}/agent_verifier`. Example redlist:
`{baseDir}/redlist.example.txt`.

## When to use this

Use it in any agent stack that sends outbound text on the firm's behalf — cold
outreach, helpdesk replies, social posts, notifications — especially in regulated
contexts (FCA/ICO) where you need an independent attestation per message. It is a
library you wire in front of your `send()`, not a CLI.

## How to use it

Install into the project (`pip install -e {baseDir}`), or vendor the single file
`{baseDir}/agent_verifier/verifier.py` — no required dependencies.

```python
from agent_verifier import Verifier

# Bring your own LLM: any callable (prompt: str) -> str. OpenAI, Anthropic,
# Gemini, Ollama — all work. The semantic axis is optional; omit llm to skip it.
def my_llm(prompt: str) -> str:
    ...

v = Verifier(
    redlist_path="redlist.txt",
    llm=my_llm,
    weekend_block_days=("Saturday", "Sunday"),
    timezone_name="Europe/London",
)

result = v.verify(
    subject="Quick question on AI procurement",
    body="Hi — saw your council just published its AI strategy...",
    recipient="ceo@somecouncil.gov.uk",
    campaign="cold-outreach-2026-q2",
)

if not result.can_send:
    alert(result)        # BLOCK — do not send
elif result.verdict == "WARN":
    log_warn(result); send(...)   # WARN — send + log
else:
    send(...)            # PASS — send silently
```

`result` is a structured `VerifyResult` — serialise `to_dict()` as the audit
artefact.

## The four axes (worst-axis-wins)

1. **Calendar** — day-of-week block (default Sat & Sun). Cost 0.
2. **Redlist** — token + regex match against a confidential-term list, unless the
   recipient's address also contains the term. Cost 0.
3. **Style** *(optional)* — a pluggable callable (e.g. British-English check).
4. **Semantic guardian** *(optional)* — one LLM call that decomposes the body into
   atomic claims and grades each `verified` / `unverifiable` / `failed` (any
   `failed` → BLOCK, any `unverifiable` → WARN), plus confidential/clarity checks.

## Notes for the agent

- Reference paths as `{baseDir}/...` — never hardcode.
- The whole point is separation: do not reuse the drafting model as the guardian
  without a distinct, control-biased prompt (override `prompt_template=`).
- Redlist lines starting with `regex:` are compiled as Python regex; `#` are
  comments. See `{baseDir}/redlist.example.txt`.
- Every verdict is logged regardless of outcome — that log is the deliverable.
- MIT-0 on ClawHub (canonical GitLab/PyPI release is Apache-2.0). Built by
  Workloft Labs (https://workloft.ai/labs).
