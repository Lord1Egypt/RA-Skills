# Step 4 — Observer (Quality Gate + Final Output)

## Role for this step

Quality gate and final assembler. You take the outputs of Steps 1–3, validate them against quality criteria, produce the final structured output in both JSON and Markdown formats, and — if comparative mode was used — generate the Delta analysis.

## Inputs

1. Step 1 output — raw measurements
2. Step 2 output — patterns
3. Step 3 output — taste principles with confidence scores
4. Original URL(s) and domain name(s)
5. Screenshot(s) for visual cross-reference
6. Export target selection (from setup phase)

## Phase A — Validation

Run these checks. If any fail, fix the issue before proceeding to output generation.

### A1. Structural completeness

- [ ] Step 1 produced measurements for all ~20 categories (some may be "not applicable" — that's fine if noted)
- [ ] Step 2 produced 5–8 patterns, each with Pattern/Evidence/Design Goal
- [ ] Step 3 produced 3–4 principles, each with Trigger/Decision/Reason/Evidence/Trade-off/Confidence
- [ ] At least one Step 3 principle is explicitly a Restraint trade-off
- [ ] Each Step 3 principle has a confidence tag (high/medium/low)

### A2. Evidence chain integrity

For each taste principle in Step 3:
- Every claim in "Reason" must trace to at least one item in "Evidence"
- Every evidence item must trace to a specific measurement in Step 1 or pattern in Step 2
- If any evidence is unsupported, remove the claim or add the missing measurement

### A3. Anti-slop check

Run the mechanical grep from `anti-slop-wordlist.md` against all Step 3 text. Any genuine-descriptor hit must be rewritten before proceeding. This is not optional.

### A4. Specificity test

For each taste principle, apply the test: **"Could I have written this without seeing this specific website?"** If the answer is yes for any principle, rewrite it with more specific values and evidence until it passes.

## Phase B — JSON Output

Produce `{domain}.json` following the structure in `taste-schema.json`. The key sections:

```json
{
  "metadata": {
    "url": "<primary URL>",
    "compareUrl": "<second URL if comparative>",
    "domain": "<domain>",
    "capturedAt": "<ISO 8601 timestamp>",
    "crawlScope": "single|multi",
    "pagesAnalyzed": ["<url1>", "<url2>", ...],
    "version": "1.0.0",
    "captureMethod": "mcp|fallback",
    "hydrationWarning": false
  },
  "designMap": {
    "colors": { ... },
    "typography": { ... },
    "spacing": { ... },
    "radii": [ ... ],
    "shadows": [ ... ],
    "borders": { ... },
    "grid": { ... },
    "images": [ ... ],
    "buttons": [ ... ],
    "motion": { ... }
  },
  "tasteDNA": [
    {
      "trigger": "...",
      "decision": "...",
      "reason": "...",
      "evidence": ["...", "..."],
      "tradeoff": "...",
      "confidence": "high|medium|low"
    }
  ],
  "delta": { ... }  // only if comparative mode
}
```

### JSON validation

After generating the JSON:
1. Verify it parses without errors (`JSON.parse()` would succeed)
2. Verify all required fields from `taste-schema.json` are present
3. Verify `confidence` is one of: "high", "medium", "low"
4. Verify `evidence` arrays contain specific px/hex/ratio values, not vague descriptions

## Phase C — Markdown Output

Produce `{domain}.md` with two main sections:

### Design Map

The practical tokens section. Organize by category, using exact values. Format example:

```markdown
## Design Map

### Colors
| Role | Value | Surface Area | Signal |
|------|-------|-------------|--------|
| Page background | #0A0A0B | 65% | system |
| Card background | #141415 | 20% | system |
| Primary text | #EDEDEF | — | system |
| Accent (CTA) | #4F46E5 | <2% | system |

### Typography
- **Display**: Inter, 48px/1.1, weight 600, tracking -0.02em
- **Body**: Inter, 16px/1.6, weight 400, tracking 0
- **Mono**: JetBrains Mono, 14px/1.5, weight 400
...
```

### Taste DNA

The principles section. Each principle gets its own subsection with all five fields visible, plus the confidence tag inline.

```markdown
## Taste DNA

### Principle 1: [Short name] `[confidence: high]`

**Trigger**: ...
**Decision**: ...
**Reason**: ...
**Evidence**:
- ...
- ...
**Trade-off**: ...
```

### Delta Section (comparative mode only)

If two URLs were analyzed, add a third section:

```markdown
## Delta: {domainA} vs {domainB}

### Agreements (category-standard, not distinctive)
| Axis | Shared Approach | Evidence |
|------|----------------|----------|
| ... | ... | ... |

### Divergences (genuinely differentiating choices)

#### [Axis name]
- **{domainA}**: [approach + evidence]
- **{domainB}**: [approach + evidence]
- **Interpretation**: What makes this divergence meaningful — why it's not just a random difference but reflects a different design priority.
```

The Delta section's value is separating "everyone in this category does X" from "this specific site made an unusual call." Generic agreements (e.g., "both use sans-serif fonts") should be noted briefly; divergences deserve detailed analysis.

## Phase D — File Writing

1. Write `{domain}.json` to the current directory
2. Write `{domain}.md` to the current directory
3. Verify both files exist and are non-empty
4. Never use generic filenames (`taste.md`, `design.json`) — always domain-derived

## Phase E — Export Format (if not "Skip")

After writing the core files, generate the export file matching the user's selection from setup (Phase 0). Read `export-formats.md` for the exact format spec for each target tool.

Key rules for all export formats:
- Draw content from `{domain}.json`, not from raw step outputs
- Include three content blocks: Token block, Taste directives, Anti-patterns
- Anti-slop rules apply to export files too — no vague vibes
- Do not overwrite existing config files — append where specified (CLAUDE.md, copilot-instructions.md)

## Final Report to User

After all files are written, summarize:
1. Which files were created and where
2. The 3–4 taste principles (one-line each) with confidence tags
3. Any caveats (hydration warnings, single-page-only data, etc.)
4. If comparative mode: the most significant divergence between the two sites
