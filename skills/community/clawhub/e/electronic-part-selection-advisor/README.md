<!-- lifecycle: asset ttl:never -->
# Electronic Part Selection & Second-Source Advisor

An AI agent skill for electronics distributors, hardware engineers, and sourcing teams.
Built to answer one question reliably: **"Can I use this part — and what will bite me later?"**

## What it does

| Capability | What the agent actually does |
|---|---|
| Part selection | Cross-checks datasheet parameters before recommending |
| Second source / alias | Proposes alternatives with the pin- and package-level caveats spelled out |
| Drop-in vs. circuit-change | Separates "just swap it" from "you must redesign around this" |
| Lifecycle & obsolescence | Flags EOL / NRND / last-time-buy risk on the candidate parts |
| Single-source risk | Marks parts where one supplier = one point of failure |
| BOM risk review | Produces a one-page risk sheet you can attach to a design review |
| Distributor reality | Checks availability and price context instead of quoting from memory |

## Why it is different

Most part-search tools just return a matching part number. This skill is built around **refusal rules**:

- Safety-certified, automotive, storage, and military-qualified parts are **on a no-substitute list** by default.
- The substitution decision flow is **8 steps and cannot be skipped** — package check, pin mapping, tolerance, operating temp, certification, footprint, variant/prefix rules, and lifecycle.
- Every claim must point at a traceable source (datasheet revision, distributor page). If the source cannot be fetched, the agent says **"unverified"** rather than guessing.
- It never invents a parameter value. Missing data is reported as missing.

> Disclaimer: this skill provides engineering reference assistance, not a procurement commitment.
> Final substitution approval always remains with the responsible engineer.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Agent instructions, hard rules, refusal criteria |
| `references/selection-rules.md` | Substitution policy, no-substitute categories, 8-step decision flow |
| `references/data-sources.md` | Approved vs. unapproved data sources, ranking of authority |

| `references/pin-to-pin-judgment.md` | Pin-to-pin judgment standard — IC / semiconductor |
| `references/connector-pin-to-pin-judgment.md` | Pin-to-pin judgment standard — connectors |

> `scripts/` holds local authoring helpers (self-check, publish) and is not part of the skill's capability.

## Intended use

Design review input, BOM hardening, shortage mitigation, distributor quoting prep.
Not intended to replace formal qualification or supplier-mandated approval.

**Do not feed it confidential customer drawings or unannounced pricing you are not authorized to share.**

---

**Publisher:** @Hegions · **Slug:** `electronic-part-selection-advisor`
**License:** MIT-0 (ClawHub platform default — per-skill license overrides are not supported) · **Version:** 1.0.0
