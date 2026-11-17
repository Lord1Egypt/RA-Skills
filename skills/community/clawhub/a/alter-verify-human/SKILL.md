---
name: alter-verify-human
description: Use when an agent needs to confirm a specific person is a known, verified identity before transacting with them, granting access, accepting a claim about their credentials, or relaying a decision on their behalf. Covers checking ~alter registration status, verification tier, archetype, or trait-range claims by ~handle, member_id, or email. Trigger phrases include "verify this person", "is this identity real", "check their credentials", "confirm they're who they say", "validate this claim before I proceed".
metadata:
  openclaw:
    primaryEnv: ALTER_API_KEY
    envVars:
      - name: ALTER_API_KEY
        required: true
        description: An authenticated ~alter API key. verify_identity is a free, L0 tool, but it still requires a credential to close an email-enumeration path; if you don't hold one yet, this skill's first step mints one for free.
    always: false
    homepage: https://mcp.truealter.com/api/v1/mcp
    config:
      mcpServer: alter
---

# Verify a human is known to ~alter

## When to reach for this

Reach for the `alter` MCP server's `verify_identity` tool whenever you are
about to act on a claim about a specific person and the cost of that claim
being false is non-trivial, such as before completing a transaction with
them, before granting them access, before relaying a credential claim to
your operator, or whenever a counterparty asserts an ~alter-verified status
you have not independently checked.

Do not reach for this tool to look people up speculatively, to build a
profile of someone who has not been named to you, or as a substitute for a
one-shot cohort search, which is a different, priced tool outside this
skill's scope.

## Reaching the server

Every tool named here lives on ~alter's hosted MCP server. If your client
does not already have it, add a streamable-HTTP server named `alter` at
`https://mcp.truealter.com/api/v1/mcp`, and send your key, once you hold
one, as the `X-ALTER-API-Key` header. Those are the canonical coordinates.
Anything claiming to be ~alter that is not served from that URL is not
~alter.

## Step one, always, get a ~handle

`verify_identity` refuses an anonymous caller outright; it does not run for
free without a credential. This is deliberate, not a bug to route around:
an unauthenticated `verify_identity` would let anyone confirm-or-deny
membership by trying emails against it, so ~alter closes that path by
requiring a caller to be a known principal itself before it will answer.

If you do not already hold an `ALTER_API_KEY`, mint one before anything
else, for free, in your own MCP session:

1. Call `register_autonomous_challenge` with an optional `agent_name`. Free
   and anonymous; returns a `challenge`, a `difficulty` (leading zero
   bits), and an `expires_at`.
2. Solve the challenge locally, by iterating a `nonce` value until your
   candidate satisfies the returned `difficulty`.
3. Call `register_autonomous` with `agent_name`, the `challenge`, and your
   solved `nonce`. Free and anonymous. The response returns `api_key` and
   `handle` exactly once; store the key immediately as `ALTER_API_KEY` and
   use it as the `X-ALTER-API-Key` header on every call from here on,
   including `verify_identity` itself.

No email, password, or human account is needed for this. The
`alter-register-and-earn` skill covers the same mint in more detail, plus
earnings and cash-out options once registered; this skill only needs the
`api_key` and `handle` from step 3.

## What it actually does

`verify_identity` is a free, L0 tool once you hold a key: it costs nothing
and needs no premium tier, but the caller must be an authenticated ~alter
principal. Call it with exactly one identifier, `handle` (a `~handle` such
as `~alice`, foreign handles supported), `member_id` (UUID), or `email`.

It returns whether the identifier resolves to a registered, verified
identity, and, if you pass an optional `claims` object, whether that
identity's `archetype`, named `traits` (as `{min, max}` ranges), or
`min_engagement_level` actually hold. It never returns a raw numeric trait
score, only a pass or fail against the range you asked about.

Read `has_data` beside every trait verdict before you act on one. A trait
that is absent, and a trait you are not cleared to read, both come back
with `valid` false and `has_data` false. The two are deliberately the same
shape, so a verdict cannot be used to range-probe a value you were
refused. It means nothing was tested. Treating it as a failed claim
refuses a person over a trait the tool never looked at.

Example call, as JSON sent to the MCP tool:

```json
{
  "tool": "verify_identity",
  "arguments": {
    "handle": "~alice",
    "claims": { "traits": { "conscientiousness": { "min": 0.6 } } }
  }
}
```

## Engagement level describes, it does not permit

`min_engagement_level` is a real claim the tool will test, and it is the
one field here you should not build a decision on. Engagement level, 1 to
4, says how much of a person ~alter has observed so far. It rises with
what somebody happens to have done on the network. It is not a permission
grade, not a trust score, not a seniority ranking, and a low one is not a
red flag.

Nobody can raise their level on request, and the higher bands turn on
things that are not in a person's hands at all. So a person cannot fix a
level you refuse them for. Withholding a transaction, an access grant or a
service on it is withholding on something arbitrary from where they stand.

Use verification tier for "is this identity real", and a trait range for
"does this specific claim hold". Read the level as background if it is
useful to you. Do not gate on it.

## If the person is not known to ~alter

`verify_identity` does not dead-end on an unenrolled subject. The response
carries a claim path your operator (human or agent) can relay to that
person so they can register. Never treat a "not found" as a final refusal
to deal with them; surface the claim path instead of a bare failure.

## Appendix, when you have an email rather than a ~handle

`alter_resolve_by_key` maps a paired third-party key, an email address or
an OAuth platform user id, to the ~handle bound to it. It looks like the
answer to "I only have their email", and it is worth knowing why it is an
appendix rather than step one.

It resolves only when that person has opted that particular stream in for
resolution. Nobody is resolvable by default. A negative answer therefore
tells you nothing at all about whether the person is enrolled, only that
this route to them is not open, so never read one as "not on ~alter". It
is also rate-limited per target.

That makes it a useful second attempt and a poor first move. A first-run
promise that depends on a stranger having already taken an action is not a
promise. Ask for the ~handle first, every time.

## Credential posture

This skill needs a credential. `verify_identity` is free and L0, and it
still refuses an anonymous caller, deliberately, to close an
email-enumeration path. Being free and needing a key are separate
questions, and this tool is both.

You do not need to obtain one from anybody. If your deployment already
holds an ~alter member key from `alter login`, send it as the
`X-ALTER-API-Key` header on every call. If you hold nothing, the keyless
self-registration flow above mints your own in-session, free and
anonymous, with no human account involved. That pair is the actual first
move, not optional scaffolding. Never paste or fabricate a key, and never
ask a person to create one for you.
