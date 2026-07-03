# agent-verifier

Pre-send verification for outbound agents.

A small, opinionated guardian that sits in front of any `send()` in your agent stack — email, social, helpdesk reply, anything. Multi-axis verification: deterministic gates (calendar, redlist, regex) plus an optional semantic check (LLM-graded confidential / claims / clarity).

> When an agent speaks for the firm, "the model was careful" is not a control.

The producer model that drafts the message cannot also be the control that approves it. `agent-verifier` is the small, separate guardian you put in front of `send()` so every outbound has an independent verdict — and a per-message log a regulator can read.

This is the reference implementation Workloft ships in front of its own outbound agent. Companion to [Workloft Research Note №05](https://workloft.ai/labs/notes/pre-send-verifier-2026-05-09.html).

## Install

```bash
pip install agent-verifier  # coming soon to PyPI; for now: clone + pip install -e .
```

Or vendor the single file `agent_verifier/verifier.py` — no required dependencies beyond the Python 3.10+ standard library.

## Quick start

```python
from agent_verifier import Verifier

# Bring your own LLM. Any provider works — OpenAI, Anthropic, Gemini, Ollama.
def my_llm(prompt: str) -> str:
    return openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    ).choices[0].message.content

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
    alert(result)            # BLOCK — do not send
elif result.verdict == "WARN":
    log_warn(result)         # WARN — send + log
    send_email(...)
else:
    send_email(...)          # PASS — send silently
```

The result is a structured `VerifyResult` you can serialise to JSON and store as the audit artefact.

## The four axes

| # | Axis | Check | Cost |
|---|------|-------|------|
| 1 | **Calendar** | Day-of-week block. Default: Saturday & Sunday. | 0 |
| 2 | **Redlist** | Token + regex match against a confidential-term list. | 0 |
| 3 | **Style** *(optional)* | Pluggable callable (e.g. BrE check, no-superlatives). | varies |
| 4 | **Semantic guardian** *(optional)* | One LLM call scoring `confidential` / `claims` / `clarity`. | one LLM token bill |

Worst-axis-wins. Any `BLOCK` aborts the send. Any `WARN` allows the send but flags it. All `PASS` sends silently. Every verdict is logged regardless.

## The redlist

A plain-text file of strings that must never appear in outbound — unless the recipient's email also contains the term (you don't redact a client's name when emailing the client). Lines starting with `regex:` are compiled as Python regex. Lines starting with `#` are comments.

See [`redlist.example.txt`](redlist.example.txt).

## Bring your own LLM

The `llm` parameter is a callable `(prompt: str) -> str`. It receives a structured prompt asking for a JSON verdict on three axes (confidential / claims / clarity).

The default prompt is in `_DEFAULT_PROMPT` — override it via `prompt_template=` if you want a firm-specific spec (e.g. an FCA-style prompt that biases toward `BLOCK` on regulatory claims).

## Why this exists

Three reasons the producer model can't be its own control:

1. **Separation of concerns.** A producer optimised to write persuasive copy is the wrong sensor for "is this appropriate?" Different incentives. Different sensors.
2. **The failure-mode space is bigger than the producer's prompt covers.** "Today is Saturday." "This codename shouldn't leak." "This claim is invented." Those aren't template problems; they're policy + reality-check problems.
3. **The auditor wants an independent attestation.** A per-message log — `drafted by X, evaluated by guardian Y across axes A1–An, verdict V, reason R` — is the artefact.

Full reasoning: [Workloft Research Note №05 — Pre-send verification](https://workloft.ai/labs/notes/pre-send-verifier-2026-05-09.html).

## Hosted version

There's also a free hosted endpoint at `https://chat-api.workloft.ai/labs-api/v1/verify` (Workloft Labs API) — useful for trying the pattern without wiring an LLM yourself. See [workloft.ai/labs/api.html](https://workloft.ai/labs/api.html).

## What's new in v0.2 (2026-05-09 evening)

Two upgrades stolen with attribution from [Indy Dev Dan's Verifier Agent video](https://www.youtube.com/@indydevdan/videos), generalised away from coding agents to outbound text agents:

- **Atomic-claim decomposition.** The semantic axis now breaks the body into 1–10 atomic claims first ("we helped 3 LAs ship X", "Anthropic shipped Opus 9", "EU AI Act enforces 2 Aug 2026") and verifies each as `verified` / `unverifiable` / `failed`. Any `failed` → BLOCK. Any `unverifiable` → WARN. Sharper signal than scoring the whole draft.
- **Flywheel feedback.** Two new fields the LLM always returns: `could_not_verify` (what it would have needed external context to check) and `needs_from_user` (what the operator could add to next-time inputs to help). Operators template these answers into the verifier's own context — the verifier improves with every send.

The `VerifyResult.to_dict()` shape gains `claims: {total, verified, failed, unverifiable, items: [...]}`, `could_not_verify`, and `needs_from_user`. Callers that don't read these still work unchanged.

**Breaking from v0.1**: the LLM prompt no longer asks for a separate `claims` PASS/WARN/BLOCK axis (it's superseded by the atomic-claim block). If you override `prompt_template`, see the new shape in `_DEFAULT_PROMPT`.

## Status

`v0.2.0` — production at Workloft (in front of Maggie's outbound cadence) since 9 May 2026. Stable interface; v0.3 will add stop-hook auto-fire over a Unix socket so one verifier can sit in front of N producers without each producer knowing.

## Contributing

Issues + PRs welcome at [gitlab.com/Alfpl/agent-verifier](https://gitlab.com/Alfpl/agent-verifier). Especially:

- Additional language `style_check` implementations (US English, German, French)
- Provider-specific LLM adapters (OpenAI, Anthropic, Gemini, Ollama)
- Rate-limit / sender-reputation axes

## Licence

This ClawHub distribution is **MIT-0** (MIT No Attribution) — ClawHub's uniform
licence for all published skills. See [LICENSE](LICENSE).

The canonical project at [gitlab.com/Alfpl/agent-verifier](https://gitlab.com/Alfpl/agent-verifier)
and on PyPI is released under **Apache-2.0**.

---

Built by [Workloft Labs](https://workloft.ai/labs) — agent infrastructure for regulated buyers. Substrate before spectacle.
