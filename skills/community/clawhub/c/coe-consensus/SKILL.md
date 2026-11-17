---
name: coe-consensus
version: 2.0.0
description: Evaluate signed votes against an operator-configured quorum.
---

# coe-consensus

Use only when the user requests this specific operation. Review SECURITY.md before running the service.

## Consensus behavior

`JEP_CONSENSUS_POLICY` maps tenant names to configuration, e.g. `{"team-a":{"policy":"simple_majority","validators":["v1","v2","v3","v4"]}}`. Optional operator fields: `trust_weights`, `threshold`, `f`. Request-supplied weights/thresholds are rejected. Trusted keys authorize proposers; only configured, independently signing validators count.

At most 128 signed events are accepted per evaluation. A V or T event must refer to exactly one earlier same-target judgment and contain `reference_digest=skill.core.event_digest(judgment)`. If an event supplies its own `hash`, it must equal `event_digest(event)`. The signature covers this reference digest and session context. One issuer contributes at most one vote per assertion; conflicting statements disqualify that issuer. Zero confidence contributes no vote. No verification means unresolved. Termination requires the original issuer.

Majority needs at least three distinct confirmations and more than half of configured membership. Weighted quorum needs three distinct confirmations and strictly more than the operator threshold (at least half of total configured weight). BFT quorum needs n >= 3f+1 and n-f confirmations. This is a stateless quorum evaluator, not a distributed BFT protocol or action executor. Re-evaluating the same round cannot multiply voters; downstream consumers must use the round ID for idempotent execution and preserve evidence if they need a durable decision ledger.

The Shared World State hash is a JCS SHA-256 checksum, not an authenticated signature or externally anchored tamper proof record. Verify signed input evidence and protect the response channel/storage. No automatic state execution occurs.

## Setup

Work from the package directory containing `skill/` and `requirements.txt`. Install locked dependencies with `pip install --require-hashes -r requirements.txt`, provision the documented authentication configuration, and run on 127.0.0.1. This package never starts a daemon or changes another runtime automatically.
