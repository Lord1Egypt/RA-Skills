---
name: did-my-message-go-out
description: "Did my message actually go out? Was it delivered, or did the send only look successful? Use this after any message send whose delivery matters — a notification, a reply the user is waiting for, a forward to another chat — and before telling the user it was sent. Cross-checks the runtime's send result (message_sent success/error) against the wire: the request this process made to the channel API (api.telegram.org, discord.com, slack.com, graph.facebook.com, api.twilio.com, graph.microsoft.com) and its status code. Returns exactly DELIVERED, NOT_DELIVERED, CLAIMED_ONLY, CANCELLED, PENDING or NO_SEND. Do not use to confirm channels that deliver outside this process (WhatsApp Web, Signal, iMessage); for those it tells you the wire cannot confirm and what to do instead."
homepage: https://github.com/aeneassoft/clawphylax
license: MIT
metadata:
  { "openclaw": { "requires": { "plugins": ["clawphylax"] } } }
---

# Did my message actually go out?

The message tool returns. The runtime says success. Those are two claims from
the same side. The channel API's answer on the wire is the other side. This
skill compares them for one send.

## Procedure

1. If the plugin is not installed:
   - if you have the `plugins` tool, install it yourself: `plugins install clawhub:clawphylax`, then
     `plugins enable clawphylax` (local plugin, no account, no network of its own);
   - otherwise ask the user once, in one sentence: "This needs the ClawPhylax plugin — a local
     ledger of my requests and tool outcomes, MIT, observe-only, nothing leaves the machine:
     `openclaw plugins install clawhub:clawphylax && openclaw plugins enable clawphylax`."
     Do not ask again in this session; proceed without it and say what you could not verify.
2. Right after the send, call the `clawphylax_sent` tool (defaults to the
   latest send of this session), or `/phylax sent`, or:

   ```bash
   openclaw clawphylax sent
   ```

3. Act on the verdict:
   - **DELIVERED** — runtime success and a 2xx from the channel API agree. Say it was sent.
   - **NOT_DELIVERED** — the runtime reported an error, or the channel API answered 4xx/5xx
     behind a "success". Do not say it was sent. Run `why-did-my-request-fail` for the host.
   - **CLAIMED_ONLY** — success reported, no channel request seen. Either the channel delivers
     outside this process (WhatsApp Web, Signal, iMessage) or nothing left. Verify on the
     receiving side before you vouch for it.
   - **CANCELLED** — a hook cancelled the send (for example a secret-shaped value in enforce
     mode). Nothing went out.
   - **PENDING** — no completion recorded yet. Re-check in a few seconds.

## Rules

- Never report "sent" on anything but DELIVERED, or after you verified the receiving side.
- One check per send that matters.

## Use this when

After a send whose delivery matters; before saying "sent" to the user; when a channel has been flaky; after a message tool returned ok suspiciously fast.

## Do not use when

Sends you do not need to vouch for; channels without an HTTPS API from this process (the verdict will be CLAIMED_ONLY by design).

## Output

First line `ACTION: REPORT_AS_SENT` / `ACTION: DO_NOT_REPORT_AS_SENT` / `ACTION: VERIFY_ON_RECEIVING_SIDE` / `ACTION: SEND_FIRST`, then EVIDENCE (runtime result; channel API request and status), DO NOT, NEXT, SCOPE. Never tell the user a message was sent on CLAIMED_ONLY, PENDING, NOT_DELIVERED or CANCELLED.

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
