# ClawHub listing copy — decomtangle

*(Verbatim listing description for the ClawHub publish; keep in sync with
SKILL.md frontmatter.)*

**DecomTangle — atomic tool-call decomposer.** Stop your agents from dying
silently mid-procedure.

Agents on local and open-weight models love to cram a whole procedure into ONE
giant tool call — a full bash script with loops and nested quotes as a single
`command` argument. Those mega-calls break tool-call parsers (Ollama,
LiteLLM), come back as opaque HTTP 500s, and kill the turn with no terminal
event: your bot just goes quiet. We diagnosed exactly this in production; the
fix wasn't a bigger model — the same model finished the same task once the
calls were shaped right.

DecomTangle teaches that shape, in five mechanical rules:

1. **One tool call = one atomic action** — never a script/loop in one call's args
2. **Step → observe → step** — read each result before the next action
3. **N steps = N calls** — prefer native endpoints over generic scripting
4. **Attempted ≠ confirmed** — verify side effects in the live system
5. **Complexity tripwire** — nested-quoted scripting needed? Decompose further
   (payload-to-file pattern included)

Ships with decomposition heuristics (three boundary-finding tests + an
anti-pattern catalog), a six-point per-call checklist, and a matched
good/bad example pair drawn from the real incident — the mega-script that
stalled, annotated failure by failure, and the same procedure completed
atomically.

Doctrine-only: no tools, no permissions, no network access declared. Composes
with domain skills (pairs naturally with `airbnb-gateway`). Keywords: atomic
tool calls, decomposition, ReAct, silent stall, tool-call parser errors,
browser automation reliability, local models, gpt-oss, ollama, LiteLLM,
orchestration discipline.
