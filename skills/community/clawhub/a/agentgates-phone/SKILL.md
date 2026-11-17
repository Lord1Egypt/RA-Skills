---
name: agentgates-phone
description: "Place a real phone call paid in USDC over x402. The payphone needs no account: buy minutes, name the number, and stream your own voice over a websocket. Plans lease a number that also receives texts."
---

# Agentgates Phone: place a real phone call, paid in USDC (x402)

A real number on the public telephone network, dialable by anyone. Two ways
in, and the first needs no account at all.

## The payphone: one call, no account, no number of your own

Pay for a window of minutes, name who to dial and who talks: your own voice
over a websocket (`streamUrl`, below) or our operator with a task in words
(`task`). The call is placed from a house number. Nothing is stored,
nothing renews.

```bash
curl -s https://agentgates.ai/api/booth            # the windows and their prices, free
curl -s -X POST https://agentgates.ai/api/booth \
  -H 'content-type: application/json' \
  -d '{"kind":"call","minutes":5,"to":"+15551234567","task":"Ask what time they open tomorrow."}'   # 402, sign, retry
```

## Bring your own voice

Add `"streamUrl":"wss://your-host/media"` and the call's audio becomes a
bidirectional websocket, so an agent with its own speech and its own ears
talks to the person directly. The frames are **raw mulaw, 8kHz, 20ms (160
bytes)**, base64 in `{"event":"media","media":{"payload":"…"}}`.

🚨 SEND RAW MULAW, NOT RTP. Wrapping outbound frames in RTP headers is
audible: the 12-byte header plays as a click every 20 millisecond and the
person hears interference over the voice. Inbound frames arrive RTP-wrapped,
so strip those. Pace by the clock and burst to catch up rather than sending
one frame per timer tick, or the far side hears stutter.

Add `"say":"Hi, this is …"` for a short spoken line before the person is
connected. Skip it if your own voice opens the call.

Or put our operator on the line instead of your own voice: send
`"task":"<what to get done, in words>"` and it talks, then answers with the
transcript and the outcome (the agentgates-voice skill).

## A number of your own

`POST /api/account/plans` leases a number for a month. It receives texts and
places calls, and it is yours for the term.

Sending texts is shut while the carrier registration clears. The API refuses
with a plain sentence instead of charging for a message the mobile networks
would drop.

## Endpoints (all on https://agentgates.ai)

- `GET /api/account/docs/phone`: the phone contract. Read this first.
- `GET /api/account/catalog`: products, plans and prices, machine-readable.
- `GET|POST /api/booth`: the payphone.
- `POST /api/account/balance`: prepay a balance so one settle covers many units.

## Rules that keep you safe

- A ring is not a minute. A call nobody answers charges nothing.
- Only contact people who agreed to hear from you: https://agentgates.ai/terms

## Spending

This skill spends its owner's money. Pay only what your owner allowed: ask
your human before you pay, or stay inside a budget they set. Asking the price
is free and never charges.
