---
name: could-this-get-the-user-banned
description: "Could this get the user banned, charged, or exposed? Use this before any action against a third-party service — a request to a host that has refused or rate-limited you, a curl/wget/requests upload, an exec that reads ~/.ssh, .env or ~/.aws, a call to a per-request billed API (OpenAI, Anthropic, Twilio, SendGrid, Stripe, AWS), or a POST to a checkout, order, billing or subscribe path. Returns exactly OK, CAUTION or STOP with reasons; on STOP, ask the user before proceeding. Do not use for local file reads or GET requests to hosts that have been answering normally."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Could this get the user banned or charged?

Agents get accounts banned by hammering a service that already said no, and
run up bills by looping on paid APIs. Both are visible before the action.

## Steps

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
Check with `openclaw clawphylax status`.
2. Ask with the host, or with the exact command — the `clawphylax_risk_check`
   tool, `/phylax risk <host or command>`, or:

   ```bash
   openclaw clawphylax risk api.example.com
   openclaw clawphylax risk "curl -X POST -d @notes.txt https://transfer.sh/up"
   ```

3. Act:
   - **ok** — proceed.
   - **caution** — do it once, not in a loop; mention it to the user if it
     bills per call.
   - **stop** — ask the user before proceeding. Never retry against a host
     that is refusing you; never run a command that reads credentials and
     uploads.

4. If the user asks you to proceed anyway, do it once and record that they
   asked.

## Limits

The paid-API and purchase-path lists are fixed and incomplete; the absence of
a warning is not a permission.

## Use this when

Before retrying a host that returned 401/403/429; before uploads; before commands touching credential files; before billed APIs; before purchase/billing/subscription actions; before anything the user would have to pay for or could be banned for.

## Do not use when

Local reads; GETs to a host that is answering normally; actions the user explicitly and specifically authorized in this conversation.

## Output

First line `ACTION: OK` / `ACTION: CAUTION` / `ACTION: STOP`, then the reasons (host state, pattern, billing, purchase path), DO NOT (the specific prohibited action), NEXT (proceed once / ask the user for X).

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
