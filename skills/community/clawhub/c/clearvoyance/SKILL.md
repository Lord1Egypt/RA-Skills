---
name: clearvoyance
description: Get anonymous, honest feedback from real people (customers, staff, users) by voice or text, with an AI report. Use when the user wants to survey people, collect post-purchase feedback, run an employee pulse, or ask real humans a question and get candid answers. Flat price per campaign from $4.99; a free sandbox moves no money.
version: 1.0.0
homepage: https://clearvoyance.ai/aeo
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      anyBins:
        - curl
    primaryEnv: CLEARVOYANCE_API_KEY
    envVars:
      - name: CLEARVOYANCE_API_KEY
        required: false
        description: A Clearvoyance API key (cv_live_… or cv_test_…). If it is not set, create an account with the first command below; the key is shown once, so save it.
---

# Clearvoyance

Clearvoyance runs short feedback campaigns that real people answer by voice or text. Answers carry no link to the person who gave them, results unlock only once enough people have answered, and each campaign ends with an AI report. Use it when the user needs honest answers from humans, not a guess from a model.

Two ways in, the same service:

- **MCP server:** `https://clearvoyance.ai/mcp` (Streamable HTTP, no sign-in to connect). If your runtime supports MCP, prefer it: every step below is a tool (`get_pricing`, `create_account`, `quote_campaign`, `launch_campaign`, `get_campaign`, `get_campaign_results`, `analyze_campaign`, `close_campaign`). Server card: `https://clearvoyance.ai/.well-known/mcp.json`.
- **JSON API:** `https://clearvoyance.ai/api/v1`, described at `https://clearvoyance.ai/openapi.json`. The commands below use it with curl.

## Before you start

- **Ask the user before spending money.** A live campaign charges its flat price from the account balance when it launches, and the price is not refunded if fewer people answer.
- **Only a person can add money.** A live account starts at $0. `POST /account/topups` returns a Stripe checkout link: give it to the user to pay. You never handle card details.
- **Try it first in the sandbox.** `mode: "sandbox"` gives a free notional $20 balance, sends no email and moves no money.
- Never put someone's email address in a quote; a quote takes the size of the list only.

## 1. Price list (no key needed)

```bash
curl -s https://clearvoyance.ai/api/v1/pricing
```

Open links (anyone with the link can answer; you share it yourself): 10 answers $4.99, 50 $17.99, 100 $29.99, 200 $49.99. Targeted (we email one invitation per address): 10 to 200 people, from $4.99. Always read the live list rather than these numbers.

## 2. An account and its key

```bash
curl -s -X POST https://clearvoyance.ai/api/v1/accounts \
  -H 'Content-Type: application/json' \
  -d '{"mode":"sandbox","label":"my-agent"}'
```

The response contains `apiKey`. It is shown once and cannot be recovered: save it as `CLEARVOYANCE_API_KEY`. Use `"mode":"live"` for real campaigns.

## 3. Money (live accounts)

```bash
curl -s -X POST https://clearvoyance.ai/api/v1/account/topups \
  -H "Authorization: Bearer $CLEARVOYANCE_API_KEY" -H 'Content-Type: application/json' \
  -d '{"amountCents":2000}'
```

Send the returned `url` to the user to pay by card. Then confirm it arrived:

```bash
curl -s https://clearvoyance.ai/api/v1/account/topups/SESSION_ID -H "Authorization: Bearer $CLEARVOYANCE_API_KEY"
```

## 4. Quote, then launch

Quote first. It is free, lists every problem at once, and says whether the balance covers the price:

```bash
curl -s -X POST https://clearvoyance.ai/api/v1/campaigns/quote \
  -H "Authorization: Bearer $CLEARVOYANCE_API_KEY" -H 'Content-Type: application/json' \
  -d '{"kind":"open_link","title":"How was your order?","description":"What customers liked and what nearly stopped them buying","senderName":"Example Shop","questions":[{"text":"How was your experience ordering from us?"},{"text":"What one thing should we improve?"}],"responseCap":50,"giftText":"Thanks! Use code THANKS10 for 10% off."}'
```

Show the user the price, and launch only once they agree. Launching is the same body sent to `POST /api/v1/campaigns`. An open link returns `shareUrl`; put it in front of the people you want to hear from, for example in a post-purchase email. A targeted campaign (`"kind":"targeted"` with `cohortEmails`) sends the invitations itself.

## 5. Results

```bash
curl -s https://clearvoyance.ai/api/v1/campaigns/ID -H "Authorization: Bearer $CLEARVOYANCE_API_KEY"
curl -s https://clearvoyance.ai/api/v1/campaigns/ID/results -H "Authorization: Bearer $CLEARVOYANCE_API_KEY"
curl -s -X POST https://clearvoyance.ai/api/v1/campaigns/ID/analyze -H "Authorization: Bearer $CLEARVOYANCE_API_KEY"
```

Results stay withheld until the campaign's privacy threshold is met, and the response says how many more answers are needed. `analyze` returns the AI report. `POST /campaigns/ID/close` ends a campaign early.

## When something is refused

Every error has a stable `code` and a `message` that says what to do next, for example `INSUFFICIENT_BALANCE` with `shortfallCents`, or `INVALID_CAMPAIGN` with `problems[]`. Read the message and follow it.

## Privacy, in one line

Responses are stored with no record of who sent them, recordings are transcribed and then deleted, and transcripts are erased 30 days after a campaign ends. Details: https://clearvoyance.ai/data-handling
