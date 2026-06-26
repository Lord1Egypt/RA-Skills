# WORKFLOW EXECUTION

> **Component** | Shared across all workflows
> Execution sequence: load scratch → scope → sources → execute → validate → deliver.
> Dependencies already read before this component is invoked (see workflow.md).

---

> **PREREQUISITES**
>
> - Sub-agent persona already embodied
> - All dependencies read (objectives, template, guides)
> - Execute all steps sequentially
> - STOP if validation fails

---

## STEP 1: LOAD SCRATCH

Check if `./workspaces/{workspace_id}/outputs/{workflow-id}/.scratch` exists.

- **Exists:** Read `.scratch` for context (scope, findings, phase from previous session).
- **Not exists:** Create `outputs/{workflow-id}/` if needed. Read `./references/core/scratch-template.md` → clone to `outputs/{workflow-id}/.scratch`.

---

## STEP 2: SCOPE CLARIFICATION

Guide: `./references/guides/scope-clarification.md`

Clarify requirements based on workflow MISSION and OBJECTIVES. Do NOT re-ask info already confirmed during orchestrator routing. User may override `Research Depth` and `Output Type` defaults from workflow.md.

- **Autonomous:** Assess info → present scope summary → proceed without confirmation
- **Collaborative:** Apply adaptive path (Fast / Selective / Full) → present scope → wait for confirmation

After scope confirmed → populate `.scratch` with scope details.

---

## STEP 3: SOURCE SELECTION

Load additional context from workspace. Optional.

1. Scan `./workspaces/{workspace_id}/outputs/*/*.md` and `documents/*`
2. Filter: exclude current workflow outputs
3. **No sources found →** skip to Step 4 silently
4. **Autonomous:** Auto-load relevant sources silently
5. **Collaborative:** Present source list, wait for user selection

---

## STEP 4: EXECUTION

Execute work to achieve MISSION and OBJECTIVES, following TEMPLATE structure.

1. Apply METHODOLOGY PRINCIPLES from objectives.md
2. Achieve all OBJECTIVES from objectives.md
3. Follow TEMPLATE structure from template.md
4. Accumulate findings continuously
5. Before writing final output: recall language settings — if uncertain or context was compacted → re-read `./references/core/core-config.md`

### Autonomous

Execute independently. Full autonomy on approach, methods, sources. Success criteria define WHAT — HOW is your decision.

**Scratch update:** When session is long and context compaction likely, append compressed key findings to `.scratch`. Update `Phase` field.

### Collaborative

Guide: `./references/guides/collaborative-research.md`

Execute with user validation at key milestones. Maintain autonomy between checkpoints.

**Scratch update:** After user confirms checkpoint (agrees with findings or adjustments are resolved), append final agreed findings to `.scratch`. Update `Phase` field.

---

## STEP 5: VALIDATION

Validate completed work before delivery:

- [ ] Mission accomplished per objectives.md
- [ ] All objectives achieved
- [ ] Output-standards guide applied (`./references/guides/output-standards.md`)
- [ ] Template structure followed correctly
- [ ] Language matches `{language_output}` with `{language_terminology}` (if uncertain → re-read core-config.md)
- [ ] Output complies with `{output_type}` specifications (±30% variance)
- [ ] VALIDATION CRITERIA from objectives.md completed

**If fails:** Return to Step 4. **If passes:** Proceed to Step 6.

---

## STEP 6: DELIVERY

1. Re-read `.scratch` for complete findings (scope, all agreed checkpoints)
2. Generate outputs per DELIVERABLES in objectives.md
3. Write files to `Output Path` from workflow.md
4. Verify file write success
5. Delete `.scratch` from `outputs/{workflow-id}/`

**Completion:** Report workflow name + output path(s) + success status.

**Collaborative additional:** Suggest follow-up workflows, highlight areas for deeper investigation.

**After delivery → control returns to orchestrator.**
