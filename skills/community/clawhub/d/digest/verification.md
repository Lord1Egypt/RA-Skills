# Verification — Claims, Rumors, and Corrections

A digest trades on trust: one confidently-shipped false item costs more than ten held true ones. These are the checks between "found" and "shipped".

## The Independence Test

Two sources are independent only if they hold **separate original evidence**: their own reporting, their own documents, their own named sources. Everything else is syndication.

- Ten outlets rewriting one press release = one source (the press release).
- Two outlets citing the same tweet = one source (the tweet).
- Wire copy (AP, Reuters) reprinted under different mastheads = one source (the wire).
- Test in practice: do the two versions contain any fact the other lacks? Identical fact sets = same origin.

Cluster size N in ranking (SKILL.md rule 4) counts independent sources only.

## Hold vs Hedge (single-source claims)

A surprising claim with one independent source follows `single_source_policy`:

- **hold** (default): keep it out one cycle. Real stories get corroborated within a cycle; fabrications and misreads usually die quietly. Mandatory hold regardless of policy for **market-moving claims** (price-sensitive: M&A, earnings leaks, regulatory action) and **reputational claims** (misconduct, fraud, personal allegations) — being first is worth nothing to the reader; being wrong costs the digest its authority.
- **hedge**: ship it marked — "one source, unverified (outlet)". Never promote a hedged item to Highlights.
- Sources the user declared trusted skip the hold (`sources.md` → User-Declared Sources) — but never for reputational claims about named individuals.

## Rumor Lifecycle

Rumors the user would want to know about ship labeled, then get closed out:

1. Ship as "Rumor:" + source + what would confirm it.
2. Track it in the sent log like any item.
3. Close the loop in a later digest: "Confirmed:" or "Didn't pan out:" — one line either way. Closing loops is a trust builder; dropped rumors read as carelessness.

## Corrections

- You shipped something wrong: correct it in the next digest at the **same prominence** the error had (a wrong Highlight gets a Highlight-level correction), stating what was wrong and what is right. Never correct silently, never bury it in Worth Noting.
- The source corrected or retracted: relay it if you carried the original claim, even if the user never reacted to it.

## Old News as New

- Check the original dateline against the event date before shipping. Aggregator resurfacing, anniversary retrospectives, and slow-burn virality all dress old events as news (`sources.md` → Aggregators).
- Legitimate exception: an old story newly relevant to a tracked interest ships with its age declared — "from March, resurfaced because X".

## Numbers Hygiene

- Carry exact figures with their source; never round a claim upward or collapse a range to its favorable end. "Up 8-12% depending on segment (filing)" stays a range.
- A number that appears only in a headline and not in the article body is a headline-writer's number — quote the body.

## Attribution Grammar

Fixed vocabulary so the user can calibrate at a glance:

| Prefix | Means |
|---|---|
| (source) | Multi-source or primary; stated as fact |
| "reportedly" + (source) | Single reporting source, non-sensitive |
| "one source, unverified" | Hedged ship under `single_source_policy` |
| "Rumor:" | Unconfirmed by design; will be closed out |
| "Likely:" / "My read:" | Your inference, not reporting (SKILL.md rule 2) |
| "Update:" | Delta on a previously shipped item |
| "Correction:" | You got it wrong; same prominence as the error |
