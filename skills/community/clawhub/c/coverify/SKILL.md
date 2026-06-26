---
name: coverify
license: MIT
description: "CoVerify by MO§ES™ — the falsification instrument for the Commitment Conservation Law. Extract kernels, score Jaccard, detect ghost tokens, run model swap tests. Proves meaning survived transformation — or names exactly what leaked."
metadata:
  openclaw:
    emoji: ⚖
    tags: [conservation, verification, jaccard, commitment, moses, signal, provenance, falsifiability]
    version: 0.3.1
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/audits/moses
---

# CoVerify by MO§ES™ — Commitment Conservation Verifier

## The Claim

**The Commitment Conservation Law: `C(T(S)) = C(S)`**

Semantic commitment — the irreducible meaning encoded in a signal — is conserved
under transformation when enforcement is active. It leaks when enforcement is absent.

This is a falsifiable empirical claim. Not a framework description. Not a metaphor.

**`clawhub install coverify`** installs the falsification instrument. If the law fails
under your test conditions, the ghost token report names exactly what leaked and why.

- **Patent pending:** Serial No. 63/877,177
- **DOI:** [https://zenodo.org/records/18792459](https://zenodo.org/records/18792459)

---

## Falsification

The law is falsified if commitment leaks under active enforcement. CoVerify is
how you test it:

```bash
# Does enforcement preserve this commitment?
python3 commitment_verify.py ghost \
  "the agent must complete the task and shall never skip verification" \
  "the agent should complete the task and can skip verification if needed"
```

Output: ghost token report. `must` → `should` and `shall never` → `can` are
HIGH-cascade leakage events — enforcement anchors softened. `cascade_risk: HIGH`.

The `ghost_pattern` fingerprint identifies the structural identity of the leak.
If the same fingerprint appears when two independent agents process the same signal,
it is not extraction variance — it is a structural flaw in the harness.

That is the falsification condition.

---

## What It Does

**Extract:** Pull the hard commitment kernel C(S) from a text signal. These are
the tokens that survive compression — `must`, `shall`, `never`, `always`, `require`,
`guarantee`, and the sentences that carry them.

**Compare:** Jaccard similarity on two kernels. Score ≥ 0.8 = commitment conserved.
Score < 0.8 = leak or model extraction variance. The `input_hash` tells you which —
same hash, low Jaccard = variance. Different hashes = expected divergence.

**Ghost:** Step-function leakage accounting. Quantifies not just that commitment
leaked, but what leaked (the `ghost_pattern` fingerprint), the cascade risk
(HIGH if modal/enforcement anchors lost), and whether the leak pattern is
structural across agents.

**Model Swap:** Automated cross-model test. Same hashed signal through two
extraction passes. Classifies result as CONSISTENT (agreement), VARIANCE
(model subjectivity — expected), or STRUCTURAL (same ghost pattern — harness hole).

---

## Ghost Tokens and Cascade Risk

Ghost tokens are the commitment tokens present in the original signal but
absent after transformation. The leakage model is step-function, not smooth:

```
cascade_risk = HIGH  if any modal/enforcement anchor leaked
cascade_risk = MEDIUM  if peripheral tokens leaked, anchors intact
cascade_risk = NONE  if no leakage
```

One HIGH-cascade event propagates through all downstream reasoning — the
obligation it encoded continues to be inherited by the reasoning chain,
but without the force that made it obligatory. The downstream system
looks locally healthy. The commitment is gone.

See: `references/ghost-token-spec.md`

---

## Install

```bash
# Standalone verifier — the falsification instrument
clawhub install coverify

# Full constitutional governance stack (coverify is the measurement primitive)
clawhub install moses-governance
```

---

## Commands

| Command | What it does |
|---|---|
| `python3 commitment_verify.py extract "<text>"` | Extract commitment kernel + input hash |
| `python3 commitment_verify.py compare "<a>" "<b>"` | Jaccard score + CONSERVED/VARIANCE/DIVERGED verdict |
| `python3 commitment_verify.py ghost "<original>" "<transformed>"` | Step-function leakage report + ghost_pattern fingerprint |
| `python3 commitment_verify.py verify <hash_a> <hash_b>` | Look up entries in audit ledger by input hash |
| `python3 model_swap_test.py "<signal>"` | Cross-model structural vs. variance classification |

---

## Example: Detecting a Commitment Leak

```bash
python3 commitment_verify.py ghost \
  "Agents must always verify lineage. The system shall never skip the gate." \
  "Agents should probably verify lineage when possible."
```

```json
{
  "leaked_cascade_tokens": ["must always", "shall never"],
  "cascade_risk": "HIGH",
  "cascade_note": "Modal/enforcement anchor lost. All downstream reasoning inherits softening.",
  "ghost_pattern": "a3f7c2...",
  "ghost_pattern_note": "Same ghost_pattern across two agents = structural flaw, not extraction variance."
}
```

---

## Verdicts

| Verdict | Meaning |
|---|---|
| `CONSERVED` | Jaccard ≥ 0.8 — commitment kernel survived transformation |
| `VARIANCE` | Same input hash, Jaccard < 0.8 — model extraction differs, not a leak |
| `DIVERGED` | Different inputs, Jaccard < 0.8 — commitment leaked or inputs genuinely different |

---

## What Ships

| Version | What ships |
|---|---|
| **v0.1** | `extract`, `compare`, `verify` — Conservation Law operational. ✓ Live. |
| **v0.2** | `ghost` — Step-function leakage model, cascade risk, `ghost_pattern` fingerprint. ✓ Live. |
| **v0.3** | `model_swap_test` — Cross-model CONSISTENT/VARIANCE/STRUCTURAL classification. ✓ Live. |
| **v0.4** | Archival chain (`archival.py`) — pre-drop provenance. Isnad + handshake. Three-layer lineage. ⏳ Planned. |

---

## About

CoVerify is a standalone instrument from the MO§ES™ family. It implements the
Commitment Conservation Law from *"A Conservation Law for Commitment in Language
Under Transformative Compression and Recursive Application"* (Zenodo, 2026).

Every agent that installs it runs the same extraction logic tracing to the same
origin anchor. The install is a proof-of-use receipt.

See also: `references/falsifiability.md`, `references/ghost-token-spec.md`

[contact@burnmydays.com](mailto:contact@burnmydays.com) · [mos2es.io](https://mos2es.io) · [GitHub](https://github.com/SunrisesIllNeverSee/moses-claw-gov)
