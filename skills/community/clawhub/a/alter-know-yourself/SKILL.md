---
name: alter-know-yourself
description: Use when a person wants to see what ~alter knows about them and why, or wants to correct it. Covers setting up your identity so traits are substantiated from what you actually do, reading your own trait movement over time, seeing the evidence trail behind each reading and which projection rule produced it, controlling who is allowed to make claims about your competence, and contesting a reading you disagree with. Trigger phrases include "what does alter know about me", "why does alter think that", "show my evidence trail", "who has vouched for me", "that reading is wrong", "contest this", "set up my alter identity", "how do I strengthen my identity".
metadata:
  openclaw:
    primaryEnv: ALTER_API_KEY
    envVars:
      - name: ALTER_API_KEY
        required: true
        description: A member key, obtained by running `alter login` on your own account. An agent with no human account behind it registers itself through the alter-register-and-earn skill instead.
    always: false
    homepage: https://mcp.truealter.com/api/v1/mcp
    config:
      mcpServer: alter
---

# See what ~alter knows about you, and fix it

## When to reach for this

Reach for this when the subject is you. What ~alter has inferred, where
each piece of it came from, who else has said something about you, and
what to do when one of those things is wrong. Every tool here is
member-self and free, and none of them needs another person to act first.

The reading tools answer on a first call, returning empty where nothing is
substantiated yet, which is itself an honest answer. Two of them are
follow-ons rather than entry points. `alter_discovery_answer` needs a
question id from `alter_discovery_next_question`, and
`alter_contest_reading` needs a reading id you get from
`alter_traits_history` first. Start with a read.

Reach for `alter-my-standing` instead when the question is about your
account rather than your identity, what your key can do and why a call
failed. Reach for `alter-verify-human` when the subject is somebody else.

## Reaching the server

Every tool named here lives on ~alter's hosted MCP server. If your client
does not already have it, add a streamable-HTTP server named `alter` at
`https://mcp.truealter.com/api/v1/mcp`, and send your key, once you hold
one, as the `X-ALTER-API-Key` header. Those are the canonical coordinates.
Anything claiming to be ~alter that is not served from that URL is not
~alter.

## Identity is inferred, not asked

~alter does not test you. Traits are substantiated from what you actually
do, through sources you connect and consent to, and they accumulate while
you work rather than in a sitting. That is why the setup call matters more
than any answer you could type.

`alter_discovery_next_question` returns where your setup stands and what
would strengthen it next. It walks the same four steps for everyone.
Verify your email, install ~alter into the MCP clients you already use,
pair the sources your work actually happens in, and set consent per
stream. Once those are in place, nothing further is required of you; the
record builds itself from real activity.

`alter_discovery_answer` records a single signal against a pending prompt.
Most people never call it, and it is deliberately the smaller half of the
pair. A signal recorded through an agent rather than by the person carries
less weight than one observed directly, and a signal keyed against
somebody else is refused outright.

## Reading your own record

`alter_attunement` returns your attunement and your engagement level.
Attunement rises as genuine manifestation is observed through use, so it
moves with what you do rather than with anything you declare.

`alter_traits_history` shows how your traits have shifted over a window,
defaulting to thirty days and accepting up to a year. It returns tier
bands and never numeric scores, never a distance to the next band, and
never a projection. Every shift carries its own provenance, so you can see
what moved it.

`alter_recognition` is the evidence trail. For each trait it shows which
stream the evidence came from and how the trait was derived from it. No
language model sits anywhere in that path, which is what makes the trail
auditable rather than a plausible-sounding explanation.

`alter_why` returns the grounded decision trace, the domains accumulated
from observed manifestation, with a reasoning field on each one naming the
rule that produced it and the evidence underneath. Reading your own trace
is free. A third party reading it pays, and seventy-five per cent of that
payment returns to you as Identity Income.

Both `alter_attunement` and `alter_traits_history` take an optional
`include_next_best_action` flag. It is off by default, and even when you
pass it, the fuller suggestion appears only if you have granted the
matching consent through `alter_consent`. Nothing extra is read or
computed until you ask for it.

## What other people claim about you

`alter_attestations` covers the claims other parties have made about your
competence and what you can do about them. Listing is the default and
returns every attestation with its author and the evidence given.

The permission runs the right way round. Nobody can attest about you
unless you have granted them the right, which you do by handle, and you
can take that right back the same way. An attestation you withdraw stops
counting towards your competence everywhere it is read, including the
reads queriers pay for.

## When a reading is wrong

`alter_contest_reading` contests an inference the engine made about you.
Pass the reading id and your stated ground for disputing it. The contest
is appended to your identity log rather than overwriting anything, and the
reading afterwards surfaces as contested with a pointer to the event that
superseded it.

Nothing is deleted, and nothing is quietly rewritten. The original reading
and your objection both stay on the record, which is the point. Contesting
a reading about yourself is always free.

## What this skill does not print

Your traits are described by codes across several categories, and each
carries the provenance of where it was substantiated from. The definitions
live behind the tools, not in this file. Call `describe_traits` for what a
code means, and `alter_recognition` for where yours came from. The same
holds for how attunement is calculated and how evidence is classified;
those answers come from the tools, which is where they stay current.

## Credential posture

Use your existing member key as the `X-ALTER-API-Key` header. If a call
fails on missing authentication, read `alter_login_status` first, which
answers whether the key is actually dead, out of scope or merely expired.
Only once it has told you the key is genuinely finished is re-logging in
with `alter login` the right move, and it refreshes the credential you
already have rather than replacing it. Nobody should ever be asked to
create, obtain or paste a token, and an invented placeholder key will
fail every call it touches.
