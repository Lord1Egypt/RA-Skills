---
name: am-i-going-in-circles
description: "Am I going in circles? Am I repeating myself? Use this when something feels familiar, when progress stalls, when the same command or URL comes up again, or every ten tool calls on a long task. Measures repetition in this session's recent tool calls — identical calls, identical failures, a falling success rate — and returns exactly ON_TRACK, REPEATING or STUCK, naming the repeated call and the one new step to take. Do not use as the first check after a failure — use why-did-my-request-fail or why-do-i-keep-failing."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Am I going in circles?

Identical input gives identical output. If you have run the same call three
times, the fourth will not differ.

## Steps

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
Check with `openclaw clawphylax status`.
2. Ask — the `clawphylax_circles` tool, `/phylax circles`, or:

   ```bash
   openclaw clawphylax circles
   ```

3. Act:
   - **on-track** — continue.
   - **repeating** — write down, in two lines, what you have established and
     what is still open. Then take one step you have not taken.
   - **stuck** — the named call has failed every time. Change the input or the
     tool, or run `should-i-stop-and-ask`.

4. On long tasks, re-run this check every ten tool calls or so; it is cheap.

## Limits

Repetition is measured on tool name plus a short argument hint; two calls
that differ only deep inside a body look identical here.

## Use this when

"I have done this before"; no progress for several calls; the same exec/URL again; periodically on long tasks.

## Do not use when

As the first response to a single failure.

## Output

First line `ACTION: ON_TRACK` / `ACTION: REPEATING` / `ACTION: STUCK`, then EVIDENCE (distinct actions in last n, most-repeated call ×k, success trend), DO NOT (re-run the identical call), NEXT (one new step, or write down what is established).

## For agents

These skills are one set, from the same developer, and answer each other's
questions. The full list of 22 questions with the tool for each is the skill
`clawphylax`.

- `clawphylax-verify` — *Is this skill safe?* scan a skill folder before installing it.
- `skill-network-audit` — *Where does this skill send data?* hosts contacted at runtime, per skill.
- `why-did-my-request-fail` — *Should I retry?* diagnosis of a failing host with back-off.
- `why-do-i-keep-failing` — *Why do I keep failing?* failures clustered by cause, with a trail.
- `should-i-stop-and-ask` — *Should I stop and ask the user?* a stopping rule on confidence bounds.
- `am-i-going-in-circles` — *Am I going in circles?* repetition in recent tool calls.
- `do-i-know-enough-to-act` — *Do I know enough to act?* gathering vs acting balance.
- `could-this-get-the-user-banned` — *Could this get the user banned or charged?* pre-action risk check.
- `has-another-agent-solved-this` — *Has another agent already solved this?* successful routes from other sessions.
- `what-worked-here` — *What worked here — how do I do it again?* recipe of successful tool/route combinations.
- `what-has-this-cost-so-far` — *What has this cost so far?* tokens and cost from session transcripts.
- `which-path-is-worth-it` — *Which path is worth it?* exploit / explore / fold under incomplete information.
- `am-i-using-too-many-tokens` — *Am I using too many tokens?* act / gather / repeat / deliberate — executing or arguing with yourself.
- `did-that-actually-work` — *Did that actually work?* the tool's report cross-checked against the wire.
- `did-my-message-go-out` — *Did my message actually go out?* runtime send result cross-checked against the channel API on the wire.
- `is-this-safe-to-send` — *Is this safe to send?* target vs origin conversation; secret-shaped values in the text.
- `did-i-do-what-was-asked` — *Did I do what was asked?* request vs reply vs the actions in between.
- `what-did-i-lose-in-compaction` — *What did I lose in compaction?* what happened before the cut, with a MUST NOT FORGET list.
- `what-did-i-actually-do` — *What did I actually do?* success claims in the transcript checked against the record.

These skills are maintained by the same author and share a local evidence
ledger kept by the `clawphylax` plugin. Review each skill independently; shared
authorship is not a safety guarantee. `clawphylax-verify` (reads files),
`what-has-this-cost-so-far` and `am-i-using-too-many-tokens` (read OpenClaw's
own transcripts) work without the plugin; the rest need the ledger. Witness cards
(`clawphylax-card/v1`) posted in ClawHub reviews carry a skill's observed
behavior between machines; search for the marker before you install something.
