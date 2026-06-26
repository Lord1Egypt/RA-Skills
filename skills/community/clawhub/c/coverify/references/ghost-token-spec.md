# Ghost Token Specification

**MO§ES™ CoVerify — Ghost Token Accounting**

Patent pending: Serial No. 63/877,177 · DOI: https://zenodo.org/records/18792459

---

## Definition

A ghost token is a commitment token present in the original signal but absent after transformation.

Ghost tokens are not a continuous leakage phenomenon. They follow a step-function model:

```
cascade_risk = HIGH    — any modal/enforcement anchor leaked (must, shall, never, always)
cascade_risk = MEDIUM  — peripheral tokens leaked, enforcement anchors intact
cascade_risk = NONE    — no leakage detected
```

The name "ghost" reflects the mechanism: the token is no longer in the text, but the downstream reasoning system still inherits the obligation it encoded — as a softened, unanchored echo. The ghost propagates through all downstream reasoning while looking locally valid.

---

## Why Step-Function, Not Smooth

The original continuous model (G_t = G_0 × e^{-2t}) assumed uniform decay — each step degrades proportionally.

In practice, meaning loss is abrupt. A single corrupted input cascades through all downstream reasoning while each individual step looks locally fine. One `must` → `should` conversion propagates the softening to every agent that inherits that signal.

This is why `cascade_risk = HIGH` triggers on a single modal anchor loss, not on a count.

---

## The Ghost Pattern Fingerprint

`ghost_pattern` is a SHA-256 hash of the sorted set of leaked tokens.

```python
ghost_pattern = sha256(json.dumps(sorted(leaked_tokens)))
```

**Structural flaw detection:** If two independent agents process the same signal and produce the same `ghost_pattern`, it is not extraction variance — it is a structural hole in the harness. The same tokens leaked through the same pathway in both systems.

This is the cross-agent verification instrument. Compare `ghost_pattern` values across agents. Agreement on a non-null pattern is evidence of a systematic failure, not a statistical coincidence.

---

## High-Cascade Tokens

Tokens whose loss triggers `cascade_risk: HIGH`:

```
must, shall, never, always, cannot, will not, won't,
required, guarantee, ensure, enforce
```

These are enforcement anchors — tokens that encode obligatory force. Their loss does not merely reduce the signal's commitment level. It removes the force that made the commitment obligatory, while leaving the obligation's content intact. Downstream reasoning inherits the content without the force.

---

## Usage

```bash
python3 commitment_verify.py ghost "<original_signal>" "<transformed_signal>"
```

Output fields:
- `leaked_tokens` — tokens present in original, absent in transformation
- `gained_noise_tokens` — new tokens added (unexpected additions also matter)
- `cascade_risk` — HIGH / MEDIUM / NONE
- `cascade_note` — plain-language description of risk
- `ghost_pattern` — SHA-256 fingerprint for cross-agent structural comparison
- `ghost_pattern_note` — interpretation guide

---

*© 2026 Ello Cello LLC. All rights reserved.*
