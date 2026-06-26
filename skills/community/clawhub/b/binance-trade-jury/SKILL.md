---
name: binance-trade-jury
description: Use this skill when the user wants to put a Binance trade thesis on trial, review whether a long or short idea deserves risk, get an APPROVE / REVIEW / REJECT verdict, inspect the three juror opinions, receive an execution playbook, or generate a Binance Trade Jury share card link.
---

# Binance Trade Jury

Use this skill to review a Binance trade thesis before it becomes a real position.

Public endpoints:

- Review API: `https://binance-trade-jury.vercel.app/api/trade-jury`
- Share image: `https://binance-trade-jury.vercel.app/api/trade-jury/share-image`

## When to use it

- The user wants a second opinion on a Binance trade idea.
- The user asks whether a long or short thesis is worth taking.
- The user wants a verdict backed by Binance market data instead of generic chat.
- The user wants a clearer entry, invalidation, and no-chase plan.
- The user wants a verdict card or social post for a reviewed thesis.

## Workflow

1. Extract the trade symbol. Accept either `BTC` or `BTCUSDT`.
2. Extract the side as `LONG` or `SHORT`. If the user does not specify, default to `LONG`.
3. Extract the full thesis text. If the user gives no thesis, ask for it.
4. Optionally extract bankroll in USD. If none is given, send `null`.
5. Run:

```bash
curl -sS -X POST https://binance-trade-jury.vercel.app/api/trade-jury \
  -H 'Content-Type: application/json' \
  -d '{"symbol":"<symbol>","side":"<LONG|SHORT>","thesis":"<thesis>","bankrollUsd":null}'
```

6. Base the answer on the returned JSON. The most important fields are:
   - `verdict`
   - `score`
   - `headline`
   - `summary`
   - `jurors`
   - `concerns`
   - `approvalConditions`
   - `playbook`
   - `shareText`
7. If the user wants a share card, build a payload with:
   - `verdict`
   - `score`
   - `symbol`
   - `side`
   - `headline`
   - `summary`
   - `primaryJuror`
   - `primaryConcern`
   - `generatedAt`

   Then URL-encode the JSON and append it to:

```bash
https://binance-trade-jury.vercel.app/api/trade-jury/share-image?payload=<urlencoded-json>
```

## Output guidance

- Lead with the verdict and why the bench reached it.
- Quote the three jurors in short form when useful.
- Keep the playbook concrete: starter, add, invalidation, no-chase, and risk cap.
- Do not invent exchange-private data or portfolio permissions. This skill uses Binance public market data only.
- If the API fails, surface the error and suggest retrying with a cleaner symbol or tighter thesis.

