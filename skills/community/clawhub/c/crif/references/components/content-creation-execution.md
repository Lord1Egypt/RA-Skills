# CONTENT CREATION — EXECUTION

> **Component** | Specific to create-content workflow
> Execution: load scratch → source → scope → direction → create → validate → deliver.

---

## STEP 1: LOAD SCRATCH

Check if `./workspaces/{workspace_id}/outputs/create-content/.scratch` exists.

- **Exists:** Read `.scratch` for context (scope, direction, findings from previous session).
- **Not exists:** Create `outputs/create-content/` if needed. Read `./references/core/scratch-template.md` → clone to `outputs/create-content/.scratch`.

---

## STEP 2: SOURCE SELECTION

> **MANDATORY** — Cannot proceed without source material.

1. Scan `./workspaces/{workspace_id}/outputs/*/*.md` and `documents/*`
2. Exclude current workflow outputs
3. Present sources sorted by time (newest first), wait for user selection
4. If user skips → STOP. Source required.
5. Load selected files, verify readable and non-empty

---

## STEP 3: SCOPE CLARIFICATION

Guide: `./references/guides/scope-clarification.md`

Assess source material and determine requirements:
1. Review source material and context
2. Identify key insights available for extraction
3. Determine gaps needing clarification
4. Clarify target audience if not stated

After scope confirmed → populate `.scratch`.

---

## STEP 4: CONTENT DIRECTION

> Must establish direction BEFORE creating content.

Propose and wait for confirmation:

```
CONTENT DIRECTION:

1. CORE MESSAGE: "{ONE thing audience must understand}"
2. TARGET AUDIENCE: Who, knowledge level, needs
3. NARRATIVE ANGLE: {Educational | Contrarian | Analysis | Story} + rationale
4. VALUE PROMISE: "{specific value audience gains}"

Confirm? (Y/modify/N): ___
```

- Y → proceed | modify → adjust, re-confirm | N → ask user's preferred direction

---

## STEP 5: CONTENT CREATION

Guide: `./references/guides/content-style.md`

Transform source research into platform-optimized content:

1. Apply content-style guide transformation: Extract → Synthesize → Interpret → Deliver
2. Follow confirmed content direction
3. Achieve all OBJECTIVES from objectives.md
4. Follow TEMPLATE structure from selected template(s)
5. Apply platform-specific optimization
6. Before writing final output: recall language settings — if uncertain or context compacted → re-read `./references/core/core-config.md`

**Scratch update:** When session is long, append direction + agreed findings to `.scratch` after user confirms.

### Output Type Constraints

| Template | brief | standard | comprehensive |
|----------|-------|----------|---------------|
| blog-article | ~1-3k words | ~3-6k words | ~10-15k words |
| x-thread | ~5-8 tweets | ~8-12 tweets | ~12-18 tweets |
| tiktok-script | ~30s | ~1-2min | ~2-3min |
| youtube-script | ~5-10min | ~10-20min | ~20-30min |

> Variance ±30% acceptable.

---

## STEP 6: VALIDATION

- [ ] Mission and objectives achieved
- [ ] Core message clear and memorable
- [ ] Hook captures attention
- [ ] All claims traceable to source research
- [ ] Platform constraints met (characters, duration, structure)
- [ ] Output within ±30% of output_type specification
- [ ] Content-style guide applied (`./references/guides/content-style.md`)
- [ ] Template structure followed
- [ ] Language matches `{language_output}` with `{language_terminology}` (if uncertain → re-read core-config.md)
- [ ] No hype language, balanced perspective
- [ ] VALIDATION CRITERIA from objectives.md completed

**If fails:** Return to Step 5. **If passes:** Proceed to Step 7.

---

## STEP 7: DELIVERY

1. Re-read `.scratch` for complete context (scope, direction, agreed findings)
2. Generate outputs per DELIVERABLES
2. Write to: `./workspaces/{workspace_id}/outputs/create-content/{template_id}-{date}.md`
3. Verify file write success
4. Delete `.scratch` from `outputs/create-content/`

**Completion:** Report output path(s) + content metrics (word count / tweet count / duration).

**After delivery → control returns to orchestrator.**
