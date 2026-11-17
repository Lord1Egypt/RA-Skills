## Description:

Generates aligned Chinese-language board deliverables for competitive analysis: a DOCX decision-spine report and a 14-slide PPT using public competitive intelligence, evidence grading, cross-validation, a 9-box benchmarking matrix, board resolutions, and monitoring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daikangjun19831230-kevin](https://clawhub.ai/user/daikangjun19831230-kevin)

### License/Terms of Use:

MIT-0

## Use Case:

Executives, general manager offices, and strategy teams use this skill to turn public competitive intelligence and approved company materials into board-ready Chinese DOCX and PPTX deliverables for consumer, agricultural, or food-manufacturing companies. It is intended for competitive-landscape refreshes, strategic decision reports, and board presentations that require consistent report and deck wording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included generation scripts contain hardcoded Yuxuan Foods example data that could be wrong for a new company.

Mitigation: Replace company-specific constants, tables, matrices, and narrative strings before generation, then rerun the DOCX/PPTX consistency checks.

Risk: Generated strategic analysis may rely on stale, inconsistent, or lower-confidence public competitive data.

Mitigation: Use the skill's A/B/C evidence grading, cross-check official company materials when available, and mark or discard conflicting public claims.

Risk: Internal PDFs may contain sensitive business information.

Mitigation: Provide only approved company materials and use them only when comfortable including that content in generated reports.

## Reference(s):

- [Decision-Spine Competitive Analysis Methodology](artifact/references/methodology.md)
- [PPT Flow Layout Engine Notes](artifact/references/engine_notes.md)
- [ClawHub Skill Page](https://clawhub.ai/daikangjun19831230-kevin/skills/competitive-analysis-board-report)
- [ClawHub Publisher Profile](https://clawhub.ai/user/daikangjun19831230-kevin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance, Files]

**Output Format:** [Chinese-language guidance plus generated DOCX and PPTX files with validation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a deep DOCX report and a 14-slide PPT deck that should remain wording-aligned and pass PPT overflow and stale-strategy checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
