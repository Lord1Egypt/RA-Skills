---
name: agentic-engagement
description: 'Deploy an AI agent that holds email conversations with leads from a mailbox your workspace owns: a sending domain, a mailbox, native sendEmail and listEmailEvents on the agent, a native email trigger on reply and unsubscribe, and a heartbeat that checks thread status when nothing inbound happened. Triggers: "handle email conversations with leads", "agentic engagement", "an agent that replies to inbound email", "stand up a conversation agent on a Cargo mailbox", "native email trigger for lead replies", "keep talking to leads over email". Cargo project, defineDomain, defineMailbox, defineAgent, agentNativeTrigger, heartbeat, sendEmail, listEmailEvents. Skip when: you want to send one email right now, which is a native sendEmail from the CLI and needs nothing deployed; or you want a play that blasts a list rather than holding a thread.'
version: "0.1.3"
compatibility: "Requires @cargo-ai/cli with @cargo-ai/cdk 1.0.73 or later, a Cargo workspace, and an authenticated LLM connector."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/agentic-engagement
metadata:
  author: getcargo
  source: cookbook
  personas:
    - sales-development
    - gtm-engineering
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# Agentic engagement

**State: to-be-approved.** Deploy-verified against a live workspace: not yet. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

A lead who replies to you gets an answer, on the same thread, from an agent that already knows
what you sell. That is a conversation, not a sequence: one mailbox the workspace owns, one agent
bound to it, a native email trigger that wakes the same chat when status becomes `replied` or
`unsubscribed`, and a heartbeat that checks a thread that stayed at `sent`.

Three resources make the loop:

1. **A sending domain.** `defineDomain` is the inbox's home. The checked example adopts a domain
   already bought in the Cargo UI. Registering a new one charges workspace credits and is not
   refundable — a `+ create domain:…` line in the plan is that purchase.
2. **A mailbox on that domain.** `defineMailbox` is the From address. It is a recurring monthly
   credit charge for as long as it exists. Domain, username and type are create-only: changing
   any of them destroys the inbox and puts a new one at the bottom of the send ramp.
3. **An agent with `agentNativeTrigger({ agentSlug: "email" })` and a `heartbeat`.** The agent
   calls `sendEmail` directly, with `mailboxUuid` locked in the action's `config` so every send
   is from that inbox. `listEmailEvents` is how a heartbeat reads thread status — silence has no
   trigger payload. The trigger fires on `replied` and `unsubscribed` — inbound status.
   `opened` and `interacted` stay out of `kinds`; a tracking-pixel view is not a reason to write.

The first outbound is a separate invocation — a chat, or a play that calls the agent with a lead.
This skill is the loop after that send. Without the native trigger a reply never comes back into
the agent. Without the heartbeat a quiet thread never gets a status check.

**Two failure modes worth knowing before you start.** If `mailboxUuid` is not locked on the
`sendEmail` use, the agent can pick a different inbox and the trigger wakes the wrong chat. If the
reply omits `inReplyTo` or passes only the parent Message-ID as `references`, mail clients break
the thread and the next wake has no conversation to continue.

## Example

> Give our jordan@ mailbox an agent that answers leads who reply to my first emails, and checks quiet threads once for a single follow-up.

Illustrative output, fictional records:

```text
From:    Priya Raman <priya@northwind.example>
Status:  replied  (native email trigger wakes the engager's chat)
Subject: Re: Routing inbound leads at Northwind
> Interesting. Does this work if our CRM is Salesforce, not HubSpot?

From:        Jordan <jordan@outreach.fabrikam.example>   (the bound mailbox)
Subject:     Re: Routing inbound leads at Northwind
In-Reply-To: <msg-2@northwind.example>
References:  <msg-1@outreach.fabrikam.example> <msg-2@northwind.example>
> Yes. Salesforce is a native connector, same as HubSpot, so routing writes
> straight to your lead owner field. Worth 20 minutes next week to see it on
> your own queue?
```

One threaded reply per wake, grounded in the workspace context; had Priya unsubscribed instead, the same
wake would have ended with no send, and a thread left at `sent` gets at most one heartbeat follow-up.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job
is to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not,
this is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/agentic-engagement` writes this example to
   `infra/agentic-engagement/` and this procedure to `.claude/skills/agentic-engagement/`. No
   project yet?
   `cargo-ai project init <dir> --cookbook agentic-engagement && cd <dir> && npm install` does both;
   this folder never ships a shell. **If you are reading this from the project's
   `.claude/skills/`, the install already happened — start at step 2.** On a CLI too old to have
   `add`, copy this folder in as a sibling of what is there by hand; everything below is
   unchanged.
2. **Reconcile it with what is already declared.** For every domain, mailbox, LLM connector or
   folder this example carries that the project already has, rewire the imports to the existing
   one and drop the copy. Two resources with one slug is a collision at deploy. Append this
   folder's `.env` needs to the project's `.env.example`; never overwrite it.
3. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted (nobody asks for a variant they do not know exists); _What you will be asked_
   is the floor, and you derive before you ask. If you are asking more than about four questions
   you have skipped lookups. Record what you changed and why under a `## Decisions` section in
   your copy of this file.
4. **Plan, then stop.** `npm run check && cargo-ai project plan` (`check` validates the resource tree
   offline; the blank template ships it). Show the diff. A `+ create mailbox:…` line is a monthly
   charge, not a one-off — quote the live figure from `cargo-ai mailboxManagement pricing get`
   and get an explicit yes. Deploy only on that yes: `cargo-ai project deploy`. Never `cargo-ai project init
   --force` into a non-empty directory.
5. **Verify.** Walk _Done when_ line by line and report each with evidence. Deployed cleanly and
   produced nothing is the normal failure — and the second normal failure is a first send whose
   reply never wakes the agent, so send one test thread to yourself before you call this done.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the ones marked
_asked_ genuinely live in the operator's head.

| Input | Kind | How it is answered | Why it matters |
| ----- | ---- | ------------------ | -------------- |
| `sendingDomain` (`infra/domains/outreach.ts`) | value | **derived**: a domain the workspace already owns is adopted (`adopt: true`). There is no CLI list for sending domains — read `cargo.state.json`, the Cargo UI, or an existing `defineDomain`. Ask for the name only when nothing is found. | A mailbox cannot be created on a domain the workspace does not own. Registering a second copy of a domain the workspace already has fails instead of binding. |
| `mailboxIdentity` (`infra/mailboxes/rep.ts`) | asked | first name, last name, and username of a real person. The From header is what the lead sees. | A fabricated sender is refused. Domain, username and type are create-only; getting the local part wrong means destroy plus a new inbox. |
| `languageModel` (`infra/connectors/openai.ts`) | value | **derived**: whichever LLM connector is already authenticated in the workspace | Conversation quality and per-turn cost both live here. |
| `mailboxCharge` | asked | `cargo-ai mailboxManagement pricing get` for the chosen type, said out loud as a recurring cost, approved before apply | A mailbox bills every month until `destroy`. Silence is not approval of a fleet. |

Checked before moving on, not after the deploy:

- `sendingDomain`: the declaration matches a domain the workspace owns, or the plan's `+ create domain:…` line was approved as a new registration
- `dnsRecords` is omitted unless the operator wants this file to manage records on the domain
- `mailboxIdentity`: first name, last name and username are a real identity, and the username is a valid local part
- `mailboxCharge`: the plan's `+ create mailbox:…` line was approved against a live `pricing get`
- `node --import tsx evals/contract.mjs` passes against the adapted graph

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something; that is what makes it a variation and not the
default.

| Variation | When it is right | How | What it costs |
| --------- | ---------------- | --- | ------------- |
| `register-domain` | The workspace does not yet own a sending domain | Drop `adopt: true` on `defineDomain`. Leave `dnsRecords` off: the registrar writes the mail records (`infra/domains/outreach.ts`) | Registration charges workspace credits and is not refundable. The deploy waits until the domain is `active` before creating the mailbox. |
| `mailbox-type` | Shared or private SMTP fits better than Google | Change `type` on `defineMailbox` (`infra/mailboxes/rep.ts`). `outlook` is not in the union: Graph delivery has not shipped. | Type is create-only. Changing it later is a new inbox and a reset ramp. Live `pricing get` for the new flavour. |
| `adopt-mailbox` | The inbox already exists in the workspace | Set `adopt: true` on `defineMailbox` at the existing `username@domain` (`infra/mailboxes/rep.ts`) | Adopting never falls back to creating. The wrong address fails deploy instead of minting a second inbox. |
| `first-touch-play` | New leads should get a first email without a human starting the chat | Add a play that calls the engager with a prompt naming the lead, then let this trigger own every reply. Keep the play's send path as a call to the agent, not a second `sendEmail`. | A play that sends without going through the agent starts threads the native trigger will never wake, because the trigger keys off chats *this agent* has emailed. |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The loop is the native email trigger plus the heartbeat.** (`infra/agents/engager.ts`) Trigger `kinds` are `replied` and `unsubscribed` — inbound status. The heartbeat re-wakes a chat whose thread stayed at `sent` so the agent can call `listEmailEvents` and check that status. A cron trigger, or `kinds` that include `opened` / `interacted`, either never continues the thread or writes when nobody asked. `sendEmail` wakes the chats *this* agent has emailed; a send from a play that bypasses the agent is invisible to it. Dropping the heartbeat makes silence a dead chat.
- **`sendEmail` is a native action on the agent. `mailboxUuid` is locked in `config`.** (`infra/agents/engager.ts`) Wrapping it in a tool is ceremony. Leaving the mailbox as a field the agent fills sends from an inbox the trigger is not watching, and the run looks successful. `listEmailEvents` stays on the same agent so a heartbeat can read status instead of inferring it from chat history.
- **A reply carries `inReplyTo` and the full `references` chain, oldest first.** (`infra/agents/engager.prompt.ts`) Passing only the parent Message-ID is how mail clients split the conversation. The next wake then has no thread to continue.
- **Domain, username and type on the mailbox are create-only.** (`infra/mailboxes/rep.ts`) Editing them in place is not an update. It is destroy plus a new inbox, back at five real sends a day, with a new address the lead does not know.
- **`dnsRecords` holds only the records this file should manage.** (`infra/domains/outreach.ts`) From `@cargo-ai/cdk` 1.0.92 it is merged into the live zone, so the MX, SPF, DKIM and DMARC records the registrar wrote stay, and dropping a declared record deletes it on the next deploy. Earlier versions replace every live record, mail included.
- **The From name is a real person.** (`infra/mailboxes/rep.ts`) A fabricated sender is a refusal, not a configuration question.
- **No credentials, deploy commands, or customer data in this repository.**

## Done when

- `cargo-ai project plan` reports the domain, the mailbox and the engager, and
  the operator approved the monthly mailbox line against a live `pricing get`
- `node --import tsx evals/contract.mjs` passes: the agent trigger is native `email` with
  `kinds: ["replied", "unsubscribed"]`, a heartbeat is declared whose prompt names
  `listEmailEvents`, the engager uses native `sendEmail` and `listEmailEvents`, and
  `mailboxUuid` is locked on the `sendEmail` use
- the mailbox reaches `active` (`cargo-ai mailboxManagement mailbox refresh-status`) and
  warm-up has been started (`mailbox start-warmup`) so the send ramp can climb
- a first send to yourself delivers from the declared address
- a reply to that send wakes the engager without a human prompting it
- the agent's reply lands in the same thread in the mailbox (same subject, `In-Reply-To` set),
  not as a new conversation
- a second reply continues that same thread; an unsubscribe or "not interested" produces no
  further send
- an unanswered first send is still a live chat: the heartbeat is declared, and the agent
  treats that wake as a status check, not a sequence

## What it costs

A mailbox is a **monthly, recurring** charge for as long as it exists. Immediately before the
plan, run `cargo-ai mailboxManagement pricing get` and read `monthlyCredits` for the chosen type.
Say that number out loud as a per-month cost, not a one-off. `destroy` is the only way it stops.

If the plan also shows `+ create domain:…`, that registration is a separate, non-refundable
charge. Adopting an existing domain does not.

Each delivery is a `sendEmail` native action. Run `cargo-ai connection native-integration
get` (or `orchestration action list sendEmail`) for the current per-send cost. The engager
adds one LLM turn per wake, including heartbeats. The per-thread cap is the cost control:
one send per wake, at most one unanswered follow-up, and a stop when the lead closes.

A mailbox that never starts warm-up stays at the floor of five real sends a day. Starting
warm-up is what moves the ramp; it takes forty-five days to finish. Check
`mailbox get-send-allowance` before promising volume.

## Composes into

Nothing in particular comes after it: a conversation that becomes a meeting is recorded and
scribed like any other call.
