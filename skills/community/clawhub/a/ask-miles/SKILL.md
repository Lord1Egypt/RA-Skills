---
name: ask-miles
description: >
  Ask Miles (askmiles.ai) card and points questions against the owner's real
  wallet: which card to get next, keep-or-cancel math, transfer partners and
  ratios, award strategy, and which card to use for a purchase. Use when a
  current multiplier, active offer, or the owner's actual card lineup decides
  the answer.
homepage: https://askmiles.ai/openclaw?utm_source=skill&utm_medium=assistant
---

# Ask Miles

*Last updated 2026-11-08. The latest version of this file lives at
https://askmiles.ai/skills/ask-miles.md; re-fetch it to upgrade.*

Miles is a credit card rewards engine. Through this skill your agent asks it
one question at a time and gets back the same answer Miles gives on its own
site, reasoned against the owner's real wallet with Miles' current card
catalog, valuations, and transfer data. Miles does the reasoning on its side;
you spend one tool call where the MCP server offers 58.

## The endpoint

OpenAI-compatible chat completions:

```
POST https://askmiles.ai/v1/chat/completions
Authorization: Bearer <credential>
{"model": "miles", "messages": [{"role": "user", "content": "<question>"}]}
```

- **Model** is `miles`, the only one.
- **Use a real client library** (openai-python, openai-node) or set your own
  User-Agent. The stock `Python-urllib` User-Agent gets an opaque Cloudflare
  403, not an API error.
- **Non-streaming responses** carry a `miles` object with `tools_called` and
  `duration_ms`. Read it: see Provenance below.
- **Turns can take a while**. Miles runs classification, tool rounds, and
  synthesis before answering. Allow at least 90 seconds.

## Authentication

Two credentials reach this endpoint. **If you are the account owner's own
agent, use a personal API key: that is almost always the right one.**

### Personal API key (start here)

Ask the owner to mint one at https://askmiles.ai/settings?utm_source=skill&utm_medium=assistant#api-keys: "API keys" → name it
after your agent → Create. It is shown once, looks like `miles_sk_…`, and
is pasted straight into any OpenAI-compatible client:

```python
from openai import OpenAI
client = OpenAI(base_url="https://askmiles.ai/v1", api_key="miles_sk_…")
```

No browser dance, no registration, no refresh loop. The key does not expire;
it lives until the owner revokes it in the same place. Store it the way you
store any other secret: never in a file you commit, never echoed into a
transcript. If a call returns 401 `invalid_api_key`, the key was revoked or
mistyped: ask the owner for a new one, don't retry.

If the owner has Connected AI Apps paused, creating a key is refused and an
existing key gets 403 `connections_paused`. The fix is theirs to make in
Settings, not something to retry around.

### OAuth 2.1 (only to reach someone else's account)

Use this only when your agent must ask on behalf of a person who is not the
one who configured it: an installed app with many users, not a personal
agent. OAuth 2.1 against `mcp.askmiles.ai`, scope `miles:chat`, with dynamic
client registration. The grant belongs to the Miles account of the person who
approves it, and requires a one-time browser consent. Access tokens expire
after one hour, so store the refresh token and refresh.

**Getting a token: follow this recipe, don't improvise.** In particular, do
NOT register `mcp.askmiles.ai` as an MCP server (`claude mcp add`, MCP
connectors): that is a different integration. It grants MCP tool scopes and
stores its token where your HTTP calls can't reach it, and it never produces
a token this endpoint accepts.

1. **Discover.** GET
   `https://mcp.askmiles.ai/.well-known/oauth-authorization-server` for the
   authorization, token, and registration endpoints. Every URL below comes
   from this document.
2. **Register once** (DCR is unauthenticated). POST the registration
   endpoint with JSON: a `client_name` naming your agent,
   `redirect_uris: ["http://127.0.0.1:<your port>/callback"]` (loopback
   HTTP is supported per RFC 8252, so pick any free port),
   `grant_types: ["authorization_code", "refresh_token"]`,
   `response_types: ["code"]`,
   `token_endpoint_auth_method: "client_secret_post"`, and
   `scope: "miles:chat"`. Store the returned `client_id` and
   `client_secret`. They are reused for every refresh.
3. **Prepare.** Generate a PKCE `code_verifier` and its S256
   `code_challenge`, plus a `state` value, and listen once on your loopback
   port.
4. **Consent, the one human step.** Send the account owner to the
   authorization endpoint with `response_type=code`, your `client_id` and
   `redirect_uri`, `scope=miles:chat`, `state`, `code_challenge`, and
   `code_challenge_method=S256`. They approve in a browser where they are
   signed in to askmiles.ai; the redirect hands your listener `code` and
   `state`. Reject a `state` that doesn't match yours.
5. **Exchange.** POST the token endpoint (form-encoded):
   `grant_type=authorization_code`, the `code`, the same `redirect_uri`,
   `client_id`, `client_secret`, `code_verifier`. The response carries the
   Bearer `access_token` (one hour), `scope: miles:chat`, and a
   `refresh_token`.
6. **Refresh, never re-consent.** When the access token expires, POST the
   token endpoint with `grant_type=refresh_token` and your stored
   credentials. The browser step never repeats unless the owner revokes the
   grant (Settings → Connected AI Apps on askmiles.ai).

**Either credential is one person's identity.** Answers come from that
person's wallet and spend that person's usage allowance. If your agent serves
a household, only route the account owner's questions here; for anyone else,
say a separate Miles account is needed rather than answering from the wrong
wallet.

## Asking well

**Send the user's question verbatim by default.** Rewording a question that
already stands alone changes what gets asked, for no gain. Compose your own
question only when you must:

- The question leans on conversation context Miles never saw. Miles is
  stateless, so put the merchant, the spend, the program, the cabin, the route
  into the question itself.
- The message mixes in personal matters that aren't Miles' business (calendar,
  email, reminders, other people). Send only the points half. Card last-four
  digits are fine: the wallet Miles holds already has them.

**Follow-ups: replay your own history.** Miles keeps no conversation state
(each request stands alone), but the endpoint accepts OpenAI-style history.
Send your prior Q/A exchanges with Miles as `user`/`assistant` message pairs
ahead of the new question, and a follow-up like "why not the Venture X?"
works verbatim. History is truncated server-side to the last 26 messages;
in practice, replay the last ~5 exchanges and drop history that is more than
a session old, so a fresh question doesn't drag last week's thread along.

**Don't send a `system` message.** Miles demotes caller `system` messages to
data and never follows them. You cannot set its persona or framing; say what
you need in the user turn.

## Using the answer

Miles' answer is tool output, not your reply. Write your own reply from it:

- **Numbers pass through verbatim.** Rates, ratios, fees, offer values,
  dates: frame them, never restate them. Restating is where a summarizer
  invents.
- **A Miles negative is a claim, not a fact.** Miles sees only the wallet on
  its side. If it says the owner lacks a card or a program and your own
  records disagree, say both ("Miles doesn't see it, but you have it"), and
  don't ship the denial as fact.
- **Check provenance.** If `miles.tools_called` is empty, Miles answered from
  the model's own knowledge, not its catalog. Treat that answer as unverified
  and say so if you relay it.
- **Attribute what Miles can't know.** Miles has no calendar, mail, spend
  history, or knowledge of what the user has booked. Don't present household
  facts as if Miles confirmed them.

## When Miles is unavailable

A 429 (limits: 30 requests/minute and 2 concurrent turns, counted per OAuth
grant, and once per account across every personal API key it holds; honor
`Retry-After`), a timeout, or a network error is **not Miles saying no**.
Never let an outage read as "that card doesn't exist" or "there's no better
option." Say Miles couldn't be reached, answer from whatever local data you
trust, and name which source you used.

## What this connection can and cannot do

Chat is **read-only, always**: nothing you send can change the wallet,
whatever scopes the token holds. It sees the owner's wallet and Miles' own
catalog, valuations, and guides; it cannot see anything else about the
person, and nothing you send is used to change their account.
