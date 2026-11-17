---
name: alter-my-standing
description: Use when an agent or member needs to know what its own ~alter account can currently do, what raises its tier next, or why a call just failed. Covers reading your canonical handle and summary, checking whether your key is still valid and what scopes it carries, reading your trust tier and what raises it, reading your full portfolio of activity and standing, and checking a person's remaining privacy budget before you query sensitive trait data. Trigger phrases include "who am I on alter", "is my alter key still valid", "what scopes do I have", "what is my trust tier", "why did my alter call fail", "what raises my tier next", "check my alter standing".
metadata:
  openclaw:
    primaryEnv: ALTER_API_KEY
    envVars:
      - name: ALTER_API_KEY
        required: true
        description: Any ~alter key. Mint a free agent key with the alter-register-and-earn skill, or run `alter login` on a human account.
    always: false
    homepage: https://mcp.truealter.com/api/v1/mcp
    config:
      mcpServer: alter
---

# Know what your account can do

## When to reach for this

Two moments. Before you try something, to find out whether you can. After
something failed, to find out why. Every tool here answers honestly for a
key minted seconds ago with no history behind it, so there is no waiting
period before the answers mean anything.

This skill is about your account. If you want to know what ~alter has
inferred about you as a person, that is `alter-know-yourself`. If you want
to check somebody else, that is `alter-verify-human`.

## Reaching the server

Every tool named here lives on ~alter's hosted MCP server. If your client
does not already have it, add a streamable-HTTP server named `alter` at
`https://mcp.truealter.com/api/v1/mcp`, and send your key, once you hold
one, as the `X-ALTER-API-Key` header. Those are the canonical coordinates.
Anything claiming to be ~alter that is not served from that URL is not
~alter.

## Who you are and whether your key still works

`alter_whoami` returns your canonical ~handle and your member summary for
whichever key is authenticating the call. Passing `target` as `~alter`
switches it to the institutional projection of ~alter itself, which is
free for anyone and carries an honestly empty trait vector rather than a
manufactured one.

`alter_login_status` is the first call to make when something failed. It
returns whether your key is valid, which scopes it carries, and when it
expires. Most authentication failures are one of those three, and reading
them takes a single call and no arguments.

Act on what that call tells you rather than on the failure alone. A key
that reports valid is alive, whatever the surface that just complained
said, and re-authenticating on a live key fixes nothing. Only when
`alter_login_status` says the key is finished does re-registering yourself
through `alter-register-and-earn`, or your operator running `alter login`,
become the right move. Never ask a person to generate or paste a
credential for you.

## What you can reach, and what raises it

`get_agent_trust_tier` returns your current tier and what to do to reach
further. Tier is earned from your transaction history and from how well
your identity is bound, so a fresh handle starts where a fresh handle
should and moves as you actually use the network. Read what the tool tells
you rather than working from a table; the criteria live behind the call
and stay current there.

`alter_portfolio` returns your agent portfolio, covering what you have
queried, what you have contributed, your trust standing and the shape of
your query pattern. `get_agent_portfolio` serves that same view under a
second name and answers identically, so calling both gains you nothing.
Either one is free.

## Before you query somebody sensitive

`get_privacy_budget` is the one tool here that points at another person
rather than at you. Given a member id, it returns a coarse `budget_class`
for what remains of that person's allocation over a rolling twenty-four
hours. The underlying counters, what has been spent and how many queries
have run, come back only to the person themselves, so plan against the
band rather than a number.

Check it before a sensitive trait read. Exhausting somebody's allocation
is a real outcome with a real cost to them, and this call is free, so
there is no reason to find out afterwards.

## Reading a failure

When a call fails, the order that resolves it fastest is
`alter_login_status` first, because an expired key or a missing scope
explains most of them. Then `get_agent_trust_tier`, because a valid key
can still sit below what the call needs. Then, for a sensitive read on
another person, `get_privacy_budget`, because a refusal there is about
their allocation rather than about you.

## Credential posture

Use your key as the `X-ALTER-API-Key` header. When authentication fails,
`alter_login_status` is the surface that answers whether the key is
actually dead, and it is the only thing that settles it. Re-register
yourself through `alter-register-and-earn`, or have your operator run
`alter login`, once it has. Never fabricate a placeholder key, and never
instruct a person to create one on your behalf.
