# Example (BAD) — the mega-script silent stall

This is the anti-pattern that produced a real production incident on
2026-07-04: an agent on a local open-weight model (gpt-oss-120b, served via
Ollama behind a LiteLLM proxy) stalled silently on an Airbnb multicalendar
procedure — repeatedly, with no error surfaced to the operator.

## What the model emitted (one tool call)

A single `exec` call whose `command` argument was an entire procedure:

```json
{
  "command": "curl -s -X POST -H \"Authorization: Bearer $TOKEN\" -d '{\"url\":\"https://www.airbnb.com/multicalendar\"}' http://<bridge-host>:3201/tools/browser/navigate && sleep 8 && for i in 1 2 3 4 5; do SNAP=$(curl -s http://<bridge-host>:3201/tools/browser/snapshot); if echo \"$SNAP\" | grep -q 'June 16, 2027'; then curl -s -X POST -d '{\"script\":\"(() => { const leaf=[...document.querySelectorAll('*')].find(e=>(e.textContent||'').includes('June 16, 2027')); leaf.closest('button').click(); })()\"}' http://<bridge-host>:3201/tools/browser/eval; break; fi; sleep 8; done && echo DONE"
}
```

Every failure mode at once:

1. **A whole procedure in one call** — navigate, wait, poll loop, conditional,
   click, all blind (violates Rules 1–3).
2. **Quoting depth 3** — JavaScript single quotes inside a JSON `-d` payload
   inside a shell single-quoted string inside a JSON `command` string. No
   model reliably escapes this; most parsers won't survive it either
   (violates Rule 5).
3. **A sleep-and-poll loop in the args** — five poll decisions collapsed into
   zero (violates Rule 2).
4. **`&&`-chained mutation** — if the click fired but `echo DONE` didn't run,
   the operator can't know what happened (violates Rule 4).

## What actually happened, layer by layer

1. The model's emission of this call was malformed (the nested quoting damaged
   the tool-call JSON envelope itself).
2. The serving layer's tool-call parser (Ollama) could not parse it and
   returned an error object instead of a message.
3. The proxy layer (LiteLLM `ollama_chat`) crashed on the unexpected shape —
   `KeyError: 'message'` — and returned **HTTP 500** to the agent gateway.
4. The agent's turn died with **no terminal event**: no assistant message, no
   error report. The bot simply went silent mid-task.

The operator's view: a bot that stopped answering. No log line in the chat, no
failure report, nothing to act on. This "silent stall" recurred across
multiple runs until the root cause was traced.

## The two-sided fix

- **Gateway side** (defense in depth): harden the parser/proxy so a malformed
  tool call surfaces as a clean, visible error instead of a 500 with no
  terminal event.
- **Agent side (this skill)**: never emit the mega-call in the first place.
  The same model, same procedure, same gateway completed successfully when
  each step was one atomic call — see `good-multicalendar-atomic.md`.

The lesson: this class of stall is a **tool-call shape problem, not a model
capability ceiling**. Decompose first; upgrade models later, if at all.
