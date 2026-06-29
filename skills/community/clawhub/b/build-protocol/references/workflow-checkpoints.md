# Workflow Checkpoints — Build Protocol 9 Steps

Each step has a completion criterion. Don't proceed until the current checkpoint passes.

## Step 1: Plan

**Checkpoint**:
- [ ] Outline exists (chapter list / section breakdown)
- [ ] Sub-agent allocation table (who writes what, parallelism decision)
- [ ] Time estimate (per sub-agent + aggregate)
- [ ] Dependency analysis (serial vs. parallel)
- [ ] Edge cases identified (e.g., "Safety chapter needs extra review")

**Anti-pattern**: Starting to dispatch sub-agents before Plan is complete.

## Step 2: Prepare

**Checkpoint**:
- [ ] Each sub-agent task spec ≤ 3,000 chars
- [ ] Content is self-contained (no "go read big_file.md" instructions)
- [ ] Constraints explicitly stated (what NOT to do)
- [ ] Acceptance criteria measurable (word count / keyword / checklist)

**Anti-pattern**: Expecting sub-agents to auto-discover requirements from other files.

## Step 3: Execute

**Checkpoint**:
- [ ] ≤2 sub-agents dispatched concurrently
- [ ] Second sub-agent has 1-3s jitter delay (avoid thundering herd)
- [ ] All expected children returned (no idle timeouts)
- [ ] No children returned stubs due to 0-token failure

**Handling failures**:
- Timeout → retry with different model
- Context overflow → split task further
- Corrupted output → redispatch

## Step 4: Assemble

**Checkpoint**:
- [ ] All deliverable files in target folder
- [ ] Naming convention consistent (e.g., `NN_topic.md`)
- [ ] No orphan `# progress:` or debug markers
- [ ] File sizes reasonable (not truncated)

## Step 5: Review (lightweight)

**Checkpoint**: Dispatch a lightweight review sub-agent to check:
- [ ] H1 count = 1 per file
- [ ] Chapter numbering continuous
- [ ] Table syntax correct
- [ ] No truncated paragraphs
- [ ] No stray progress markers

Expected time: 5-10 min. If >15 min, something is wrong.

## Step 6: Audit (deep) ⚠️ UNMISSABLE

**Checkpoint**: Dispatch an Audit agent (or main-agent fallback) with the 6-layer checklist:

| Layer | What to verify |
|---|---|
| L1 Facts | Citation count + no duplicates + dose sanity + brand info accuracy |
| L2 Consistency | Brand verdicts don't contradict across volumes |
| L3 Completeness | All required sections present; both male/female if applicable |
| L4 Safety | All required safety keywords present (medical); surgery/pregnancy warnings |
| L5 Format | H1 layer / table / code block / links syntax |
| L6 Anti-Sycophancy | 🔴 negatives present and realistic |

**Audit output**: `00_audit_report.md` with verdict per file.

## Step 7: Fix

**Checkpoint**:
- [ ] All 🔴 issues resolved
- [ ] 🟡 issues documented in errata list (v1.x Changelog)
- [ ] **Re-run Step 6 audit** to catch fix-induced new issues
- [ ] 🟢 issues explicitly acknowledged (not forgotten)

**Anti-pattern**: Fixing and immediately publishing without re-audit. Fixes can introduce new duplicates or inconsistencies.

## Step 8: Publish

**Checkpoint**:
- [ ] Format converted (md → docx / pdf)
- [ ] Uploaded to target location
- [ ] VERIFY: download back and open, check rendering
- [ ] Links / Table of Contents updated
- [ ] Version number in title / changelog

**For feishu docs specifically**:
- Upload goes to root → Move to target folder → List and verify

## Step 9: Errata

**Checkpoint** (after deliverable is in use):
- [ ] Subsequent issues noted with location and severity
- [ ] Append to Changelog (don't silently edit source)
- [ ] Bump version (+0.1 for minor, +1.0 for major)
- [ ] Previous version archived to HistoryBackup

**Golden rule**: Erratum is transparent revision. It's not a failure; it's honesty.
