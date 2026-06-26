# Changelog

## v1.3.2 — 2026-06-02

### Changed
- Slug renamed: `agent-research-harness` → `ai-research-harness` (old slug preserved as redirect)
- Display name fixed: "Research Harness Sync" → "research-harness"

## v1.3.1 — 2026-06-01

### Added
- **Theoretical Alignment: ETCLOVG Mapping** — Cross-referenced against Li et al. (2026) *Agent Harness Engineering: A Survey* seven-layer taxonomy; identified two coverage gaps (Observability trace-native recording, Verification path-quality evaluation) as v1.4.0 candidates
- **Actionable supplements**: Observability module, path evaluation, evaluator trustworthiness, and harness decoupling audit patterns for future versions

### Changed
- SKILL.md version bump: 1.3.0 → 1.3.1
- Minor text refinements in Core Philosophy and Phase 2 Design sections

## v1.3.0 — 2026-05-26

### Added
- **Sixth cognitive discipline**: Theoretical Grounding Before Design — every design decision must trace to published precedent or stated hypothesis
- **Seventh governance rule**: Methodology Review Gate — "novel" designs require Design Justification Document before execution
- **Eighth non-negotiable**: No non-trivial design enters execution without a Design Justification Document
- **`references/methodology-grounding.md`** — Theoretical grounding framework for schema, scoring, and experiment design (template + 2-example requirement)
- **Design justification section** in Phase 2 — Required workflow step with template reference
- **Paper search strategy library** bundled with skill distribution

### Changed
- Cognitive disciplines: 5 → 6
- Governance rules: 6 → 7
- Non-negotiables: 7 → 8
- Phase 2 Design section expanded with grounding requirement
- `references/agent-collaboration.md` updated with Methodology Review Gate details

## v1.2.0 — 2026-05-12

- New scoring principle: Metric Fairness Annotation (`evidence_access_required` flag per metric)
- New technique: Gold checklist separation (`planning_gold` vs `evidence_gold`) for fair multi-group evaluation
- New pattern: Artifact Creation QA (scaffold → validate → commit micro-cycle for agent-generated knowledge artifacts)
- New governance upgrade: **Claim-level evidence** — each factual statement in an artifact must have a traceable claim row before card text is written. Claim-first workflow documented in `references/repo-architecture.md`
- `references/scoring-statistics.md` expanded: Score Family Separation → Metric Fairness Annotation
- `references/repo-architecture.md` expanded: Artifact Creation QA section with claim-level governance + claim-first workflow

## v1.1.0 — 2026-05-12

- New governance rule #6: Calibrate Before Scaling (claim-safe memo + provenance fix before expansion)
- New non-negotiable #7: no closed loop expands without calibration
- New Phase 4 deliverable: claim-safe memo (supported findings / positive signals / not-yet-supported / required next evidence)
- Multi-level audit pattern added to Phase 1 Harden (default vs strict mode)
- Score family separation added to scoring-statistics.md (planning/evidence/correctness/specificity/traceability)
- Derived representation traceability added to repo-architecture.md invariants
- Governance-before-scale principle added to Core Philosophy

## v1.0.0 — 2026-05-10

- Initial release distilled from real-world AI-native research execution practice
- Five reference modules: repo architecture, experiment design, scoring/statistics, scientific thinking, agent collaboration
- Core workflow: Phase 0 Scaffold → Phase 1 Harden → Phase 2 Design → Phase 3 Execute → Phase 4 Handoff
- Six non-negotiables and five cognitive disciplines for agent-led research
- Domain-agnostic: applicable to any field using LLM-based controlled experiments
- SKILL.md as lean index; detailed content in references/ (no duplication)
- Clean frontmatter with agent_created flag for proper skill lifecycle management
