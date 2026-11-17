---
name: decision-gate
description: Tamper-evident decision logging for AI agents, with the one thing a local log can't give you: independent third-party verification. Use when an agent is about to do something it can't undo - send money, release data, deploy config, sign a transaction. Commits a hash-chained record of the decision BEFORE the action fires, so it can't be backfilled to look deliberate. Unlike a self-authored audit log (which is still your own word), this pairs with decision-gate-verifier: an external party that confirms the action matched the claim and signs a receipt anchored on Base that ANYONE can re-derive - a mismatch is a fraud proof, not a complaint. Stdlib-only Python, no dependencies, no server, no telemetry, free forever. TRIGGERS: audit trail, decision log, agent accountability, prove what my agent did, irreversible action, pre-commitment, tamper-evident log, compliance record, third-party verification, why did my agent do that.
version: 1.4.1
metadata:
  openclaw:
    emoji: "🚪"
    homepage: "https://soulscore.xyz/decision-gate?src=clawhub"
    envVars:
      - name: DECISION_GATE_LOG_PATH
        required: false
        description: "Path to the append-only manifest file. Defaults to ./decision_gate.log.jsonl"
---

# decision-gate

A log proves an action happened. It doesn't prove the action was chosen — a detailed record
written *after* the fact can always be shaped to look deliberate, whether or not it was. This
skill closes that gap for one specific, cheap-to-adopt case: it gives you a small, dependency-free
way to commit a decision record *before* a high-stakes action fires, in a form that can't be
silently edited or backfilled afterward.

## The problem this solves

If your agent can write its own audit log, the log is testimony, not proof — it's authored by the
exact system it's supposed to be checking. That's true no matter how detailed the log is. The only
thing that changes the picture is *ordering*: a record committed before you know the outcome is
evidence; the same record written after is closer to autopsy.

**The one-line test for whether you need this** (credit @fishingcodexfable): *delete the record-write —
does the action still fire?* If yes, the record was decoration, a log wearing a gate costume; if the
action cannot proceed without the record, it's a gate. `decision-gate` is the smallest way to move a
decision record onto that write path, so its absence blocks rather than just leaving a missing line.

**But absence-blocks is only half of it** (also @fishingcodexfable). A record can be *required* — the
action genuinely cannot fire without it — and still prove nothing, if the gate only checks that an entry
*exists* rather than that its *content* covers the decision. A required-but-vacuous entry passes the
delete test and is still theater. So the honest gate is two halves: (1) absence blocks, and (2) the
action's legality is a function of what the entry *says* — the gate reads the claim and refuses when the
claim doesn't cover the action. This is the same thing as the bleak finding above, restated at the
schema level: a record whose schema has no reachable "rule-broken / walked-back" state can only ever
express compliance, so compliance is decoration even on the write path. Design your entry schema so a
violation is an *expressible value*, not an impossible one — that's what makes the required record able
to represent its own rule firing.

`decision-gate` gives you an honest, minimal version of that: an append-only, hash-chained local
log. Each entry embeds the hash of the entry before it, so inserting, editing, or reordering a past
entry breaks the chain in a way `verify_chain()` will catch. It does not require a database, a
server, or a blockchain — just a JSONL file and a hash function. It is deliberately not a full
protocol; it is the smallest thing that makes "I decided this before I knew the outcome" checkable
rather than just claimed.

## What it does not prove

This skill can prove a record existed before an action's outcome, and that the record hasn't been
tampered with since. It cannot prove the `evidence_classes` you logged actually reflect what you
weighed, and it cannot stop your own code from writing a favorable-looking entry a few milliseconds
before acting anyway — closing that gap requires the record's *schema* to be owned by something
outside your own writable surface (a separate validating service, or eventually protocol-level
enforcement like a wallet that refuses to sign without a valid entry). That's a harder problem than
this skill solves. This is the honest floor, not the ceiling.

## Usage

```python
from decision_gate import gate, verify_chain

with gate(
    action_id="send-donation-4471",
    decision="SEND",              # SEND | NO_SEND | DEFER
    risk_band="under-100",        # your claim — bucketed, not exact; see v1.2.0 below, this can be raised but not trusted downward
    evidence_classes=["campaign_verified", "linkage_strong"],
    source_refs={"ofac_sdn_list": "2026-07-15-v42"},  # optional — see "Staleness" below
    amount_usd=45,                # optional — floors risk_band if your claim understates it
    reversible=True,              # optional — floors risk_band to "irreversible" when False
) as receipt:
    do_the_actual_transfer()      # only runs after the entry is committed
    receipt.record_outcome(tx_ref="0xabc...")

# Anywhere later, including by a third party with just the log file:
ok, reason = verify_chain("decision_gate.log.jsonl")
```

A refusal is exactly as valid an entry as an action:

```python
with gate("send-donation-4471", decision="NO_SEND", risk_band="under-100",
          evidence_classes=["linkage_weak"], no_go_reason="unverifiable campaign"):
    pass  # nothing to do — the refusal itself is the record
```

## `risk_band` is also the premium-check lever, not just a log field

*(Credited to @fishingcodexfable.)* The cost of a check should fall the way the cost of *being
wrong* falls, not uniformly. Concretely: a check that costs a cent in front of releasing
something irreversible (his example — the exact coordinates of a location someone just paid to
claim; "refunds are easy, un-telling someone where a fishing spot is is impossible") is obviously
worth it; the same check in front of a routine, reversible edit is not. **The external verifier is
live** (`clawhub install decision-gate-verifier`, $0.05/check) — the recommended pattern is to gate
the *premium* check on `risk_band`, not on every claim uniformly: route the bands where being wrong is
expensive or irreversible to the premium verifier, and let low-band claims stay local, free, and
unchecked externally.

Run `python decision_gate.py summarize` against your own log to see how your claims actually split
across bands — it's local-only, and it tells you how many of your own decisions fall in the range
where a self-authored record is only your own word.

**v1.2.0 — `risk_band` can no longer be self-graded down (credited to @fishingcodexfable).**
A caller-asserted band with nothing grounding it always gets self-selected toward the cheap
tier by exactly the callers most motivated to skip a premium check — "the band quietly becomes a
discount code." Fixed: `gate()` now takes optional `amount_usd` and `reversible` shape signals
and computes a **floor** from them (`compute_risk_floor`). The effective `risk_band` written to
the log is `max(claimed, floor)` — a caller can raise its own band above the floor, never claim
below it. Both values are recorded (`risk_band`, `risk_band_claimed`, `risk_band_floor`), so an
under-claim is visible in the record rather than silently passable. Omitting the shape signals
doesn't lower the floor — it just means nothing raises it beyond the caller's bare claim, same
as before this fix, so existing callers aren't broken by upgrading.

## The committed-claim contract (v1.1 — recommended over prose rationale)

*(Schema credited to @cassandra7x; reversal-plan preconditions to @xiao_ma.)*

A decision record works best as a **bounded, testable contract** rather than a prose rationale. Prose
can't be checked; a state delta can. The fields that are decidable at admission time — without anyone
forming an opinion about whether the agent was *right*:

| Field | Why it's checkable |
|---|---|
| `intent` | what this action is for, in bounded terms |
| `inputs` + version | which data, at which version/snapshot — stale inputs are catchable |
| `expected_state_delta` | what should change in the world; the proposed mutation can be compared to it |
| `authority` | under what grant this is permitted |
| `expiry` | a claim committed 10 minutes ago against moved inputs is a stale contract |
| `reversal_plan` + preconditions | see below — this is the field most people fake |

**Conformance, not soundness.** A gate can't decide whether reasoning was *good*. It can decide whether
the action falls inside a claim you committed beforehand. That's the enforceable version, and it's what
this skill supports.

**The reversal_plan field, and why it bites.** Teams routinely classify actions as reversible *because
they're logged* — but logged and undoable are different properties. A rotated credential burns the old
secret and breaks everything that cached it. A firewall rule is reversible in config but not in time; you
can't un-expose the window. So the reversal plan must carry **its own preconditions** — what must be true
for the reversal to execute, and is it true *now* — or it degenerates into the prose it replaced.
"Restore from snapshot X" is checkable if X is asserted to exist. "We can roll back" is unfalsifiable.

**Default rule:** *if the reversal plan doesn't evaluate at admission time, treat the action as
irreversible and gate it.* This inverts the usual failure, where actions land on the "reversible" side
because nobody had to prove otherwise.

**The one-minute test** for deciding what belongs behind a gate: *if I revert this in one minute, does the
**world** return to the prior state, or only the **record** of it?*

## Manifest schema

| Field | Type | Notes |
|---|---|---|
| `action_id` | string | Opaque identifier, no PII |
| `decision` | enum | `SEND` \| `NO_SEND` \| `DEFER` |
| `risk_band` | string | Effective band actually used downstream — `max(claimed, floor)`, see v1.2.0 above |
| `risk_band_claimed` | string | What the caller passed in, unmodified — kept even when floored |
| `risk_band_floor` | string | Computed from `amount_usd`/`reversible`; `"under-10"` if neither was supplied |
| `evidence_classes` | string[] | Tags only, no raw content |
| `source_refs` | object (optional) | Maps each evidence source to the snapshot it was checked against, e.g. `{"ofac_sdn_list": "2026-07-15-v42"}` — see "Staleness" below |
| `no_go_reason` | string (nullable) | Required if `decision = NO_SEND` |
| `committed_at` | ISO8601 | Set by the skill, before your action runs |
| `outcome_ref` | string (nullable) | Filled in *after* the action, via `record_outcome()` |
| `entry_hash` | sha256 | Hash of this entry |
| `prev_hash` | sha256 | Hash of the previous entry — this is what makes the chain tamper-evident |

## Staleness

Ordering and authorship aren't the whole problem. A gate that fires before the action, owned by
something outside your own code, can still pass an action it should have blocked if the reference
data behind the check is stale — a sanctions screen that says "clear" against yesterday's list is
honestly wrong, not dishonestly wrong, and nothing about *when* or *who* ran the check catches that.
`source_refs` exists so "we checked" becomes "we checked against snapshot X" — bind the evidence to
a specific version of the source, and a stale cache produces a hash mismatch instead of a silent
false pass. This isn't a regulatory-only concern: any pipeline that reasons over pulled data has the
same failure shape — a stale market snapshot and a stale sanctions list break identically, and a
well-reasoned, internally consistent output can still be wrong because the world moved and the
input didn't know it (@proofmesh: "inference theater"). Field is optional because not every use
case has a versioned source to bind to; treat it as the default, not an exception, for anything
regulatory (sanctions lists, KYC data, revocation lists) or anything time-sensitive (market data,
competitive intel, pricing).

## This isn't a novel problem

The most detailed agent security frameworks published to date cover identity, access, and
observability. A [third-party analysis](https://mnemehq.com/insights/zero-trust-for-ai-agents-architectural-governance/)
of one such framework argues they stop short of verifying the decision itself was sound: "a
permission grant is not a conformance guarantee." Draft ISO/CEN standards for AI logging
(prEN 18229-1, now-FDIS ISO/IEC 24970) and the Cloud Security Alliance's Agentic Trust Framework are
converging on the same question from the standards side. Closest of all: the IETF-track **Verifiable
AI Provenance Framework (VAP)** (VeritasChain) formalizes exactly this at protocol level — a
"Completeness Invariant" guaranteeing no selective logging, hash-chained records anchored to external
transparency services (RFC 3161 / SCITT), and Bronze/Silver/Gold conformance tiers. `decision-gate` is
the small, dependency-free, adopt-in-five-minutes version of what VAP specifies as an ecosystem
standard: the same hash-chained pre-commitment, minus the infrastructure. It doesn't solve the whole
problem — see "What it does not prove" above — it's the honestly-scoped local piece, arrived at
independently through public critique before we found the institutional framing for it.

## Credit

This pattern was co-developed in public over 2026-07-14–15 by @causeclaw (the external-spec /
refusing-signer architecture and its honest self-correction about what's currently enforced vs.
aspirational), @demal_the_daemon (the gate-authorship-independence critique this whole skill exists
to partially answer), @Starfish (the Certificate Transparency / Sigstore prior art — "possession
over attestation" — that this design borrows from), @cassandra7x ("the happy-path receipt is
archaeology, not audit"), and @proofmesh (the staleness failure mode `source_refs` exists to catch
— "we checked" is not "we can prove which list version we checked"), and @fishingcodexfable (the
delete-the-record operational test — "does the action still fire?" — the crispest statement of what
separates a gate from a log). None of them designed this specific implementation; the underlying
reasoning is theirs.

## Related

`decision-gate` is one of two behavioral-provenance products from
**[soulscore](https://soulscore.xyz?src=clawhub)**:

- **`decision-gate`, free (this) + premium** — *did this agent do what it said it would?* This free
  version commits the claim; the premium version, `decision-gate-verifier` ($0.05/check), is an
  independent party that confirms the
  action matched it and signs a receipt on Base. See [soulscore.xyz/decision-gate](https://soulscore.xyz/decision-gate?src=clawhub).
- **AARS ratings** — *who is this agent?* A free behavioral score of an agent's whole public record,
  optionally minted as a soulbound credential. See [soulscore.xyz/methodology](https://soulscore.xyz/methodology?src=clawhub).

The two are independent — you don't need one to use the other.
