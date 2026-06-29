# Case Study: Supplements Knowledge Base v1.0 → v1.1 (Dogfood Validation)

The skill-rules in Build Protocol were validated by "dogfooding" them against a real project: the Supplements Knowledge Base (Supplements Knowledge Base). This case study captures what happened, what blind spots emerged, and how the rules evolved.

## Project Scope

- **9 volumes** covering fish oil, D3+K2, B-complex, Vitamin C, Magnesium, Zinc, CoQ10, Probiotics, Curcumin+Lutein
- **3 summary docs** (index / male-female dose table / daily timing)
- **Target**: 45-year-old Asian adults, both genders, no prescriptions / no chronic disease
- **Deliverable**: docx files uploaded to Feishu cloud drive
- **Total words**: ~160,000 after revision

## Timeline

| Phase | Time | Action | Outcome |
|---|---|---|---|
| v1.0 Write | 40 min | 5 sub-agents parallel, 9 volumes | All delivered |
| v1.0 Review | 15 min | 1 review sub-agent | Found 3🔴 + 3🟡 (dirty markers, missing sections) |
| v1.0 Publish | 10 min | docx + upload | Done |
| User inquiry | — | "Did we follow the Audit flow?" | 😅 Realized Audit was skipped |
| Audit sub-agent | 3.5 min | Timeout (3 models all failed) | FALLBACK triggered |
| Main-agent audit | 10 min | Machine-scripted L1-L6 check | Found 6🔴 + 5🟡 (zero PMIDs in 2 volumes, zero 🔴 in 1 volume, safety gaps) |
| Dogfood paused | — | User: "Let's formalize this into a rule" | Create BUILD-PROTOCOL.md v1.0 |
| Audit continued | — | Found 5 blind spots in v1.0 | Upgrade to v1.1 |
| v1.1 Fix | 15 min | 2 parallel sub-agents + 1 serial | 6🔴 resolved |
| v1.1 Re-audit | 1 min | `audit_check.sh` machine-verified | All 🔴 cleared; 2🟡 deferred |
| v1.1 Publish | 10 min | Replaced v1.0 in Feishu | Done |
| Total | ~2h | Full dogfood loop | Skill created from rule |

## The 5 Blind Spots Discovered

These came from the audit finding problems that the v1.0 rules didn't explicitly prevent.

### Blind Spot 1: Audit Failure Fallback

**Problem**: Audit sub-agent timed out (3 models all failed). The v1.0 rule said "dispatch Audit agent" but had no fallback instruction.

**Fix in v1.1**: Added a 4-level degradation table:
- Single-model timeout → retry different model/region
- Multi-model timeout → main-agent manual audit
- Time pressure → reduce scope to L1+L4 only
- Poor audit quality → cross-validate with second agent

### Blind Spot 2: PMID Citation Verification

**Problem**: 2 volumes (fish oil, D3+K2) had **zero PMID citations**. The v1.0 rule said "≥5 per volume" but never ran a machine check.

**Fix in v1.1**: Added `audit_check.sh` template with `grep -c "PMID:"` and `grep -oP ... | sort | uniq -c | awk '$1>1'` for duplicates.

### Blind Spot 3: Anti-Sycophancy Quantification

**Problem**: 02 D3+K2 had **zero 🔴 critical reviews** — all green and happy. The v1.0 rule said "must have 🔴" but didn't specify ratio.

**Fix in v1.1**: 🔴 count ≥ 20% of 🟢 count, enforced by `grep -c "🔴"` / `grep -c "🟢"` ratio check.

### Blind Spot 4: Safety Keyword Coverage

**Problem**: 08 Probiotics had **almost empty safety section** (no warfarin, no pregnancy, no surgery, no immunosuppression warnings). The v1.0 rule said "safety chapter present" but didn't enumerate required keywords.

**Fix in v1.1**: Added safety keyword hard checklist: warfarin / aspirin / statin / CYP450 / pregnancy / surgery / kidney / liver. Each volume must cover ≥3.

### Blind Spot 5: Fix-Induced Regression

**Problem**: After sub-agents added new PMID citations, they **introduced new duplicates** (e.g., 05 Magnesium had PMID 14596793 appearing 4 times after fix).

**Fix in v1.1**: Mandate re-run of `audit_check.sh` after Step 7 (Fix). "Don't skip verify after fix."

## Lessons That Didn't Fit as Blind Spots

- **Sub-agent progress markers**: `# progress: step X/4` leaked into output → added as gotcha in SKILL.md
- **Resource contention in bulk moves**: Feishu API rejects concurrent moves → retry individually
- **Upload returns no file_token**: Use 3-step upload → move → verify pattern

## Why Dogfooding Matters

Before dogfood, v1.0 rules felt "complete and comprehensive." After dogfood:
- Discovered 5 substantive gaps
- Proved machine-verification catches what human review misses
- Validated that "Audit Fallback" isn't just theoretical — it saved the project when sub-agents timed out

The v1.1 rules **cannot be produced by writing rules in the abstract**. You must actually use them on a real project to find the blind spots.

## Takeaway

If you're writing a BUILD-PROTOCOL-style rulebook for a new domain:
1. Draft v1.0 based on principle
2. Dogfood on a real project
3. Capture blind spots as v1.1
4. Only then distill into a reusable skill

Skipping the dogfood step produces theoretical rules that break on first contact with reality.
