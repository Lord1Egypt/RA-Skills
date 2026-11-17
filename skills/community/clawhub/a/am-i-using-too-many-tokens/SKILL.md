---
name: am-i-using-too-many-tokens
description: "Am I using too many tokens? Am I spending tokens to refute myself instead of executing? Am I overthinking? Use this every ten turns on a long task, when a good first idea seems to be drifting, when several text-only turns have passed without a tool call, or when the user asks why this is taking so long. Classifies this session's assistant turns from the transcript into act, gather, repeat and deliberate, attributes output tokens, finds deliberation streaks and repeated identical calls. Returns exactly EXECUTING, RETURN_TO_PLAN or STOP_REPEATING with the next call. No plugin ledger needed. Do not use in the first three turns."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Am I using too many tokens?

The question is not how many, but what for. Tokens that act or gather move the
task; tokens that re-run a call you already made verify what you already had;
tokens that only argue with the previous paragraph distort a good first idea.

## Steps

1. Ask — the `clawphylax_token_use` tool, `/phylax tokens`, or:

   ```bash
   openclaw clawphylax tokens --window 60
   ```

   (Reads OpenClaw's own transcript of this conversation; the plugin's ledger
   is not needed.)

2. Act on the verdict:
   - **executing** — continue; the allocation is healthy.
   - **deliberating** — you have produced text without testing anything for
     several turns. Return to the plan you had before the deliberation began
     and run its first step. Let the result decide, not another paragraph.
   - **churning** — you keep re-running identical calls. Their answer will not
     change. Treat the result as settled and build on it; if you distrust it,
     change one input, not the same call again.

3. Tell the user in one line what share of the work was action, and what you
   will do differently now.

## Limits

Classification is by tool name and arguments; a turn that both reads and
writes counts as acting. Output tokens require a provider that reports usage;
otherwise turns are counted instead.

## Use this when

Every ten turns on long tasks; after several text-only turns; when the plan is drifting; when asked why this takes so long.

## Do not use when

The first three turns; tasks that are legitimately analysis-only and the user asked for analysis.

## Output

First line `ACTION: EXECUTING` / `ACTION: RETURN_TO_PLAN` / `ACTION: STOP_REPEATING`, then the shares (act / gather / repeat / deliberate), the longest deliberation streak, the repeated calls, NEXT (the first step of the plan you had, or the settled result to build on).

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
