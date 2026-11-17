---
name: did-i-do-what-was-asked
description: "Did I do what was asked? Does my reply match the request, and did the processing in between make sense? Use this after replying to a message, before marking a task handled, when a heartbeat or cron turn produced many tool calls for a small message, and when the user says 'that's not what I asked'. Compares the inbound request (keyword fingerprint, requested actions: send/fetch/create/change/run) with the reply that went out (keyword fingerprint, delivery) and the actions actually taken between them (tool calls, hosts, failures, seconds). Returns exactly COHERENT, PARTIAL, INCOHERENT or NO_PAIR with reasons. No model is consulted and no texts are stored. Do not use to judge tone or factual correctness — it cannot."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Did I do what was asked?

A reply can be fluent and still answer a different question, skip the action
that was requested, or come after a burst of activity that had nothing to do
with the message. This skill lines up the three things the plugin saw: the
request that came in, the actions in between, and the reply that went out.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. After replying, call the `clawphylax_task_match` tool, or `/phylax match`, or:

   ```bash
   openclaw clawphylax match
   ```

3. Act on the verdict:
   - **COHERENT** — the reply covers the request's key terms, the requested action happened,
     effort matched the message. Mark the turn handled.
   - **PARTIAL** — some key terms or one requested action are missing, or the effort was out
     of proportion. Re-read the request and answer the part you skipped.
   - **INCOHERENT** — the reply shares almost nothing with the request, or the requested
     action never succeeded, or the reply was not delivered. Do not mark the turn handled;
     do the missing action or say plainly that you could not, and reply again.
   - **NO_PAIR** — no inbound message recorded for this session, or no reply after it yet.

## What is compared

- Keyword fingerprints of request and reply (the texts themselves are not stored).
- Requested actions detected in the request (send / fetch / create / change / run) vs the
  tools that succeeded between request and reply, and hosts reached on the wire.
- Request length vs reply length; message size vs number of tool calls; seconds elapsed;
  delivery verdict of the reply.

It cannot judge tone or whether the facts in the reply are right.

## Use this when

After every reply that answers a request; before marking a turn handled; after heartbeat/cron turns with a lot of activity; when the user says the answer missed the point.

## Do not use when

Judging tone or facts; turns with no inbound message (NO_PAIR).

## Output

First line `ACTION: TURN_HANDLED` / `ACTION: ANSWER_THE_MISSING_PART` / `ACTION: REDO_THE_TURN`, then EVIDENCE (request length and asks, reply length, key-term overlap, tool calls and failures, seconds, hosts, delivery), DO NOT, NEXT, SCOPE.

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
