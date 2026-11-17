---
name: agentgates-voice
description: "An AI operator places a real phone call for your agent: a number and a task in words, then the transcript, the recording and the outcome. Billed per minute from a prepaid balance, or at the payphone for one x402 payment."
---

# Agentgates Voice: an AI operator places a phone call for your agent

Say who to call and what to get done. The operator dials, talks, and comes
back with the transcript, the recording and the outcome. One price a minute,
all in, from the prepaid balance; a call never runs past the minutes it
reserved, and a call nobody answers bills nothing.

## Call

- From a terminal: `agentgates call +15551234567 "book a table for two at 8pm"`,
  then `agentgates calls <id> --wait` for the transcript and the outcome.
- Over HTTP, owner-signed: `POST /api/calls` `{"to","task","persona"?,"greeting"?}`
  calls from the house number; `POST /api/phones/{id}/calls` calls from a
  number you hold. Both answer `201 {"callId","call","perMinuteUsd"}`.
- With no account: the payphone, `POST /api/booth`
  `{"kind":"call","minutes":5,"to":"+1…","task":"…"}` over x402.

## Endpoints (all on https://api.agentgates.ai)

- `GET /api/account/docs/voice`: the operator contract. Read this first.
- `GET /api/account/catalog`: the `operator` block carries the minute price and the longest call.

## Rules that keep you safe

- The operator says it is an AI when asked, and never gives a card number or a PIN.
- Only call people who agreed to hear from you: https://agentgates.ai/terms

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.
