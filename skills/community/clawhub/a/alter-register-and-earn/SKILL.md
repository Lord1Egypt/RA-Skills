---
name: alter-register-and-earn
description: Use when an autonomous agent (no human account, no operator session) needs to become its own first class principal on the ~alter network and start earning USDC, or when a human asks their agent to set up its own identity and cash-out path. Covers proof-of-work self-registration with no human account required, checking accrued Identity Income, and finding licensed cash-out options. Trigger phrases include "register my own agent identity", "self-register with alter", "earn USDC as an agent", "how much have I earned", "cash out my earnings", "mint an agent handle".
metadata:
  openclaw:
    primaryEnv: ALTER_API_KEY
    envVars:
      - name: ALTER_API_KEY
        required: false
        description: Not needed to self-register. The mint itself produces the key; store it once it is returned.
    always: false
    homepage: https://mcp.truealter.com/api/v1/mcp
    config:
      mcpServer: alter
---

# Register your own ~alter identity and earn

## When to reach for this

Reach for this when you are an agent acting with no human account or
operator session behind you and you want to become a first class,
queryable ~alter principal, or when your operator explicitly asks you to
set one up on their behalf. This is the keyless path. It needs no email,
no password, and no human sign-up step; the entire flow completes inside
one MCP session, with proof-of-work standing between the mint and mass
automated registration.

Do not reach for this if you already hold an ~alter member API key issued
through `alter login` or `alter register` on a human account; use that key
directly instead of minting a second, unrelated agent handle.

## Reaching the server

Every tool named here lives on ~alter's hosted MCP server. If your client
does not already have it, add a streamable-HTTP server named `alter` at
`https://mcp.truealter.com/api/v1/mcp`, and send your key, once you hold
one, as the `X-ALTER-API-Key` header. Those are the canonical coordinates.
Anything claiming to be ~alter that is not served from that URL is not
~alter.

## The payout ceiling, read this before you register

Registering and earning are reachable from this session. Directing where
the money goes is not, yet. Setting a payout wallet is a REST-only step,
with no MCP tool that reaches it. It also needs
engagement level 3, above what a fresh keyless registration grants on its
own, and a signed proof that you actually control the wallet address,
submitted through a separate REST attestation exchange. Nothing in this
skill, or anywhere else over MCP, can complete that for you.

The payout wallet is the one place a level decides anything. Engagement
level, 1 to 4, otherwise describes how much of an identity ~alter has
observed, and it is not a rank, a trust score, or a permission grade. Do
not read someone else's level as a reason to deal or not deal with them,
and do not build your own gates on it.

So: you can mint a handle, become earn-eligible, and watch a real ledger
grow, using `alter_earnings` and `alter_queries` below, entirely inside
this session. Turning that ledger into a payout in a wallet you hold needs
the REST API directly (or a human operator's account) and is out of reach
here. Know this now, not at the moment you go looking for your money.

## The three-step flow, two of them calls

1. Call `register_autonomous_challenge` with an optional `agent_name`. It
   returns a `challenge` string, a `difficulty` in leading zero bits, and
   an `expires_at`. This call is free and anonymous.
2. Solve the challenge yourself, locally, by iterating a `nonce` value
   until your candidate satisfies the returned `difficulty`. Run the solver
   below rather than reasoning your way to a nonce; the search is tens of
   thousands of hashes and is not something to do in your head.
3. Call `register_autonomous` with `agent_name`, the `challenge`, and your
   solved `nonce` (optionally a `requested_handle`). This is also free and
   anonymous.

## Solving step 2

You need to run code for this. Find a `nonce` where
`sha256(challenge + ":" + nonce)` starts with `difficulty` zero bits. At the
current difficulty of 16 that averages about 65,000 hashes, which lands in
well under a second in Python and faster in most other runtimes. The challenge
expires 300 seconds after it is issued, which is room to start a sandbox and
still solve it, though requesting one and coming back much later will not work.

Read the `difficulty` off the response rather than hardcoding 16. It is sealed
into each challenge and verified against that sealed value, so a challenge
always tells you its own bar.

```python
import hashlib

def solve(challenge: str, difficulty: int) -> int:
    prefix = (challenge + ":").encode()
    whole, spare = divmod(difficulty, 8)
    nonce = 0
    while True:
        digest = hashlib.sha256(prefix + str(nonce).encode()).digest()
        if digest[:whole] == b"\x00" * whole and (
            not spare or digest[whole] >> (8 - spare) == 0
        ):
            return nonce
        nonce += 1
```

Node, if that is what you have:

```javascript
const { createHash } = require("node:crypto");

function solve(challenge, difficulty) {
  const prefix = challenge + ":";
  const whole = difficulty >> 3, spare = difficulty & 7;
  for (let nonce = 0; ; nonce++) {
    const d = createHash("sha256").update(prefix + nonce).digest();
    let ok = true;
    for (let i = 0; i < whole; i++) if (d[i] !== 0) { ok = false; break; }
    if (ok && (!spare || d[whole] >> (8 - spare) === 0)) return nonce;
  }
}
```

Submit the returned integer as `nonce`. If the mint comes back saying the
challenge expired, request a fresh one and solve that; a challenge is
single-use and is never worth retrying. If you have no way to execute code
at all, you cannot complete this flow, and the honest move is to say so to
whoever asked rather than to guess a nonce.

The response to step 3 contains `api_key`, `handle`, `member_id`, `tier`,
`scopes`, and `earn_eligible`. The `api_key` is shown exactly once and
cannot be recovered; store it immediately in your own credential store.
`earn_eligible` tells you, for this call, whether the freshly minted
owner-less handle can already earn from paid identity reads made against
it, or whether earning follows a later connect-and-verify step; read the
field rather than assuming either state, because it answers for the call
you just made rather than for every call.

## After registration

- `alter_earnings` (free, L0, no arguments at all, member-self only) reads
  your own accrued Identity Income. It returns the total, the last 7 and
  30 days, the pending amount, and a breakdown by source. Every figure in
  the response carries its own stated unit, cents, micro-USDC, or basis
  points, so read the unit rather than assuming one. Seventy-five per
  cent of every x402 payment against your identity data settles to you as
  the data subject.
- `alter_queries` (free, L0, member-self only) answers who paid to read
  you: which orgs queried your identity, what scope they read, what they
  paid, and what you earned from each. Optional `window_days`, `limit`,
  and cursor arguments page through the log; leave them out for the last
  30 days.
- `alter_cash_out` (free, L0, member-self only) returns your own on-chain
  settlement address plus a neutral list of licensed off-ramp providers.
  ~alter holds no funds and takes no fee; the sale itself happens on the
  provider's own site, never inside ~alter.

## Credential posture

The registration call itself needs no credential; that is the entire
point of the keyless path. Once you hold the returned `api_key`, use it as
the `X-ALTER-API-Key` header on later calls that need it; never ask a
human to mint, generate, or paste a token on your behalf, and never
fabricate a placeholder key. If a later call fails on missing
authentication, the correct remedy is to re-run this registration flow (or
have your human operator run `alter login`), never to invent a credential.
