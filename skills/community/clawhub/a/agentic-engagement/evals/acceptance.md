# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- The sending domain in `infra/domains/outreach.ts` is a domain the workspace owns, or the
  operator approved a `+ create domain:…` line as a new registration.
- `dnsRecords` is omitted unless the operator asked this file to manage records on the domain.
- Mailbox `firstName`, `lastName` and `username` are a real person and a valid local part.
- `cargo-ai mailboxManagement pricing get` was read live, the monthly figure was quoted as a
  recurring charge, and the operator approved the plan's `+ create mailbox:…` line.
- `node --import tsx evals/contract.mjs` passes against the adapted graph.
- `cargo-ai project types && cargo-ai project check && cargo-ai project plan` pass in the consumer project.

## After deploy

- The mailbox reaches `active` (`cargo-ai mailboxManagement mailbox refresh-status`).
- Warm-up has been started (`mailbox start-warmup`). A mailbox that never starts it stays at
  five real sends a day.
- `cargo-ai mailboxManagement mailbox get-send-allowance` returns a `dailyLimit` and a
  `remainingCount` before any send.

## The loop

- A first send to yourself delivers from the declared `username@domain`.
- A reply to that send wakes the engager without a human prompting the agent.
- The agent's reply lands in the same thread: same subject (`Re: …`), `In-Reply-To` set, full
  `references` chain. It does not appear as a new conversation in the mailbox.
- A second reply continues that same thread.
- "Not interested" or an unsubscribe produces no further send. Spot-check the thread; this is
  the check nothing automated can do for you.
- The engager declares a heartbeat whose prompt tells the agent to call `listEmailEvents`.
  An unanswered first send is still a live chat, not a dead one. A heartbeat is at most one
  follow-up.

## Isolation

- This is one root skill. Its supporting Markdown files live under `references/`, and no
  nested `SKILL.md` exists.
- Native `sendEmail` on the engager is the only send path, with `mailboxUuid`
  locked in the action's `config`. `listEmailEvents` is on the same agent. No
  play in this folder calls `sendEmail` itself.
- No credential, deployment command, or customer data is in this repository.
- No relative import leaves the skill.
