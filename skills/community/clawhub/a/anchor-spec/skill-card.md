## Description:

Tiered project anchors for AI coding agents. Tier a project (T0 zero-anchor / T1 seed card / T2 full anchor), maintain it with a three-layer information model (snapshot README ≤150 lines, append-only EVOLUTION, raw log), and let anchor-doctor automate lifecycle care (cold-storage banners, distillation, archiving). Trigger on: new project / continue / resume / where were we / project anchor / seed card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lankongtongmeng](https://clawhub.ai/user/lankongtongmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use anchor-spec to choose a lightweight or full project-memory structure and maintain project context across sessions. It provides tiering rules, anchor templates, and an optional lifecycle auditor for reviewing project anchors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because of broad activation phrases and reported file writes during modes described as dry-run or read-only. Confidence is medium, and scan coverage is incomplete.

Mitigation: Review whether the project-anchor workflow is needed, check the activation phrases and reported writes before use, and account for the partial scan coverage when reviewing the skill's behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lankongtongmeng/skills/anchor-spec)
- [Anchor templates](references/templates.md)
- [Maintenance rules](references/rules.md)
- [Quality checklists](references/quality.md)
- [anchor-doctor lifecycle auditor](doctor/anchor-doctor.py)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Markdown anchor files and plain-text audit reports; optional Python lifecycle auditor]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Anchor size guidance: SEED.md ≤10 lines and README.md ≤150 lines.]

## Skill Version(s):

0.1.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
