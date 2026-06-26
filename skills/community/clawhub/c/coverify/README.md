# coverify

## The Commitment Conservation Law, runnable

> C(T(S)) = C(S) — commitment is preserved under transformation when enforcement is active. Lost when it isn't.

This skill makes that verifiable. Install it, run it on any signal, get a cryptographic score. No governance harness required.

- **Patent pending:** Serial No. 63/877,177
- **DOI:** [https://zenodo.org/records/18792459](https://zenodo.org/records/18792459)
- **Contact:** [contact@burnmydays.com](mailto:contact@burnmydays.com)

---

## Why This Exists as a Standalone Skill

The governance harness (`moses-governance`) is the constitutional enforcement layer — posture gates, audit chains, role hierarchy. That's a full stack.

`coverify` is the measurement instrument. It answers one question: **did the meaning survive?**

A researcher validating the Conservation Law doesn't need the full harness. An agent running drift checks on its own outputs doesn't need posture controls. Cornelius-Trinity wanting to run the model swap test doesn't need to install constitutional governance to do it.

```bash
clawhub install coverify
```

That's it. The Conservation Law as a single install.

---

## What You Get

**`extract`** — Pull the hard commitment kernel from any signal. These are the tokens that survive compression under the First Law: `must`, `shall`, `never`, `always`, `require`, `guarantee`, and the sentences that carry them. Returns the kernel + a SHA-256 input hash of the raw signal.

**`compare`** — Jaccard similarity on two kernels. Tells you how much commitment survived a transformation. Distinguishes commitment leak from model extraction variance by checking whether the input hashes match.

**`verify`** — Look up two entries in the audit ledger by their input hashes. Confirm both agents started from the same raw signal before comparing what they extracted.

---

## The Isnad Layer

Before extracting anything, hash the raw signal:

```
input_hash = SHA-256(raw_signal)
```

This is Isnad Layer 0 — provenance of the signal itself, separate from who processed it. Two agents on different models run `extract` on the same text. Both produce an `input_hash`. If hashes match and Jaccard is low, that's model extraction variance — not a leak. If hashes differ, divergence is expected.

Without the input hash, you can't tell the difference. With it, you can.

---

## Install

```bash
clawhub install coverify
```

---

## Quick Start

```bash
# Extract commitment kernel
python3 commitment_verify.py extract "Agents must always verify lineage before executing."

# Compare original to a transformed version — does meaning survive?
python3 commitment_verify.py compare \
  "Agents must always verify lineage before executing." \
  "Agents should probably check lineage when convenient."
```

Jaccard score 0.0 → the soft version has no hard commitment markers. Meaning did not survive.

---

## Verdicts

| Verdict | What it means |
|---|---|
| `CONSERVED` | Score ≥ 0.8 — the kernel survived |
| `VARIANCE` | Same input, low score — model extraction differs (not a leak) |
| `DIVERGED` | Different inputs, low score — meaning leaked or inputs genuinely differ |

---

## Roadmap

| Version | What ships |
|---|---|
| **v0.1** | extract, compare, verify. ✓ Live. |
| **v0.2** | Ghost token accounting — quantify how much meaning leaked, not just that it did |
| **v0.3** | Model swap test harness — automated comparison across models on identical hashed signals |
| **v0.4** | Inter-agent handshake envelope — standard format for kernel exchange between agents |

---

## Part of the MO§ES™ Family

| Skill | What it does |
|---|---|
| `moses-governance` | Constitutional enforcement harness — modes, postures, roles, audit chain |
| `lineage-claws` | Trust gate — cryptographic chain back to origin anchor |
| `coverify` | Conservation Law instrument — extract, score, verify |

[contact@burnmydays.com](mailto:contact@burnmydays.com) · [mos2es.io](https://mos2es.io) · [GitHub](https://github.com/SunrisesIllNeverSee/moses-claw-gov)
