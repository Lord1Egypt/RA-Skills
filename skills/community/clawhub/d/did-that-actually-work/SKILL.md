---
name: did-that-actually-work
description: "Did that actually work? Did my last action take effect, or did it only look like it did? Use this after any tool call whose effect matters — an exec, a write, a POST or PUT, a message send, a fetch you will build on — and before reporting success to the user. Cross-checks what the tool reported (ok/error) against what the wire showed for that same tool call: status codes (403, 5xx), empty 200 bodies, unsent uploads, no observable request at all. Returns exactly CONFIRMED, SILENT_FAILURE, UNVERIFIED or FAILED with the mismatch named. Do not use for reads you will not act on."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Did that actually work?

A tool's return value is what the tool claims. What happened on the wire is a
different fact: the POST answered 403, the 200 had no body, the upload never
left. Agents build on the claim. This checks the fact.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. Right after the action, call the `clawphylax_did_it_work` tool (defaults to
   the last non-diagnostic tool call), or `/phylax check`, or:

   ```bash
   openclaw clawphylax check
   ```

3. Act on the verdict:
   - **CONFIRMED** — the wire agrees with the tool. Build on it.
   - **SILENT_FAILURE** — the tool said ok, the wire said no. Treat the action as
     not done. Run `why-did-my-request-fail` for the host before retrying.
   - **UNVERIFIED** — no observable request (child process, local file). If the
     effect matters, verify it directly: fetch the resource, list the file,
     read the reply.
   - **FAILED** — the tool itself failed. Fix, then retry once.

## Rules

- Never report "done" to the user on UNVERIFIED or SILENT_FAILURE.
- One check per action that matters; do not check reads you will not act on.

## Use this when

After exec, write, POST/PUT/DELETE, message or any fetch you will build on; before telling the user "done"; when a result looks too easy.

## Do not use when

Reads you will not act on; diagnostic calls; when the tool itself already returned an error (then fix that).

## Output

First line `ACTION: BUILD_ON_IT` / `ACTION: TREAT_AS_NOT_DONE` / `ACTION: VERIFY_DIRECTLY` / `ACTION: FIX_THEN_RETRY`, then EVIDENCE (what the tool reported, what the wire showed), DO NOT (proceed as if it succeeded), NEXT, SCOPE. Never claim success to the user unless the verdict is CONFIRMED or you verified the effect directly.

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
