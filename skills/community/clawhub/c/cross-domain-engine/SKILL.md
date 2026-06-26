---
name: cross-domain-engine
description: Discover hidden correlations between disparate research domains using EVEZ OODA loop architecture. Use when finding novel cross-domain connections, detecting emerging technology intersections, cross-referencing threat patterns, identifying investment signals, or mining unclaimed innovations across fields. Covers signal observation, cross-domain scoring, verifiable correlation events, and append-only spine protocol.
version: 1.0.0
author: "@EvezArt"
tags: [evez, correlation, research, cross-domain, discovery, ooda, spine, maes]
---

# EVEZ Cross-Domain Correlation Engine

Discover hidden correlations between disparate research domains.

## When to Use

- Finding novel cross-domain connections nobody else would think to cross-reference
- Detecting emerging technology intersections before they're obvious
- Cross-referencing threat patterns across cybersecurity, finance, and materials science
- Identifying investment signals from undervalued research intersections
- Mining unclaimed patent territory between fields

## Architecture

The engine runs an EVEZ OODA loop:

1. **OBSERVE** — Scan domains, collect signals with intensity scores and keywords
2. **ORIENT** — Score cross-domain pairs by keyword overlap × intensity × base novelty
3. **BRANCH** — Generate verifiable correlation events with confidence scores
4. **ACT** — Commit to append-only spine (no edits, no deletes)
5. **COMPRESS** — Hash-chain the cycle into the immutable ledger

## Key Concepts

- **Spine Protocol**: Every event is written once. No updates. No deletes. The history IS the state.
- **Correlation Events**: Carry unique ID, confidence score, domain classification, and cryptographic hash
- **poly_c = τ × ω × topo / 2√N**: The EVEZ formula for topological proximity scoring
- **MAES Pattern**: Inspired by the autonomous discovery of 0.82 correlation between VQC research and FinCEN SAR patterns

## Verification

Every correlation event can be:
- Verified by checking the hash chain
- Audited via the append-only spine
- Falsified through the VERIFIED/PENDING/INVESTIGATING status system

## Formula

```
poly_c = τ × ω × topo / 2√N
```

Where:
- τ = temporal weight (recency of signals)
- ω = domain weight (importance of each domain)
- topo = topological proximity (keyword overlap between domains)
- N = number of observed signals (normalization factor)

## References

See `scripts/correlation_engine.py` for the full implementation.
