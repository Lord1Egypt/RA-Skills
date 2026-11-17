# Reference — Decomposition heuristics

How to find the atomic boundaries in a procedure before you execute it.

## The three tests

Run a candidate tool call through these; failing any one means it should be
split.

### 1. The observable-action test

*Does this call perform exactly one action whose outcome I can observe in the
result?*

"Navigate to the calendar" — one action, observable (page title / URL in the
result). "Navigate, wait for load, find the cell, click it, and report the
label" — four actions; three of them happen blind inside the call. Split into
four.

### 2. The decision-point test

*Between any two things this call does, would a competent operator look at the
intermediate state before continuing?*

If yes, that look is a decision point, and decision points are call
boundaries. Polling is the canonical case: after each read you decide
"ready → act" or "not ready → read again." A scripted
`while ! ready; do sleep 5; done` collapses every one of those decisions into
zero — you have no idea which iteration failed or why.

### 3. The failure-isolation test

*If this call errors, will I know which action failed?*

A one-action call that errors tells you exactly what broke and leaves the
system in a knowable state. A five-action call that errors leaves you with
"somewhere in there, something broke, and steps 1 through k may or may not
have happened" — which for side-effecting steps means you can no longer
safely retry anything.

## The quoting tripwire (mechanical, always-on)

Count the quoting depth **within the argument value you are about to emit**.
The JSON tool-call envelope itself does not count — every call has that.
Depth 0 (no quoting inside the value) and depth 1 (quoted tokens inside a
command string, e.g. `curl -H "Authorization: Bearer $TOKEN" -d @/tmp/x.json`)
are fine. **Depth ≥ 2 — a quoted payload that itself contains quoted strings,
inside the value — is the tripwire** (e.g. a `-d '{"script":"…'…'…"}'` inline
JSON body whose script contains its own quotes). Parsers (shell, JSON, the
gateway's tool-call extractor) fail disproportionately on exactly these
emissions, and local/open-weight models mis-escape them disproportionately
often.

Standard defusals:

- **Payload-to-file**: write the complex payload (JSON body, script text) with
  a write/file tool — write tools take raw content and need no escaping — then
  reference the file in the next call (`curl -d @/tmp/payload.json …`).
- **Split the pipeline**: `fetch | parse | act` as three calls, passing the
  small extracted value forward, instead of one piped one-liner.
- **Use the native endpoint**: if a dedicated tool exists for the action
  (click by ref, read by selector), use it instead of scripting the equivalent.

## When a single call IS enough

Atomicity is not maximal fragmentation. One call is correct when it is:

- a single idempotent read (`GET` one resource, read one file, one snapshot);
- a single well-formed command with no internal sequencing (`ls -la <dir>`,
  one `grep` over one file);
- a genuinely atomic operation the tool itself guarantees (one database
  transaction exposed as one tool op).

Piping is acceptable within one call when it is a pure read-side filter with
no side effects and trivial quoting (`curl -s <url> | grep -m5 pattern`) — the
pipe is reducing output size, not hiding sequence.

On **rate-limited surfaces**, atomicity still holds but pacing should coarsen:
wait longer between polls (a standalone wait as its own call), don't respond
to rate pressure by re-bundling actions into bigger calls.

## Anti-pattern catalog

| Anti-pattern | Why it fails | Atomic replacement |
| --- | --- | --- |
| Multi-step bash script as one `command` arg | Parser-hostile emission; blind execution; unfixable on error | One call per step |
| `sleep`-and-poll loop inside a call | Collapses every poll decision; call runs to timeout opaquely | Read → decide → read again, one call each |
| `&&`-chained mutations (`do A && do B && do C`) | If B fails, did C run? Is A safe to retry? Unknowable | Sequential calls, observe between |
| Heredoc / inline script generation | Depth-≥2 quoting; near-certain escaping damage | Payload-to-file, then act on the file |
| "Do the whole procedure and tell me at the end" | No terminal event on mid-procedure death — the silent stall | Step → observe → step; report at every milestone |
| Giant read (dump entire page/dataset into the result) | Floods context; degrades every later decision in the loop | Targeted read of the one value needed |
