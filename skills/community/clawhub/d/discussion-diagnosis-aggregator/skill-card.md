## Description:

Aggregates six single-skill Discussion diagnosis outputs into one scored, severity-tagged Markdown report in the conversation language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, and academic writing reviewers use this skill to combine six Discussion-section diagnostic outputs for an English psychology paper into one prioritized report. The report consolidates duplicate issues, assigns severity, highlights strengths, and recommends top fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is narrowly useful for aggregating English psychology Discussion-section diagnostics and may be unsuitable for other genres, sections, or disciplines.

Mitigation: Use it only after six relevant Discussion diagnosis outputs are available, and review the final report for fit to the target writing context.

Risk: Broad Chinese trigger phrases may activate the skill unexpectedly.

Mitigation: Review trigger configuration during installation and narrow or rename triggers when deploying alongside other academic-writing skills.

Risk: One merge-rule reference should be clarified, which can affect how duplicate cross-dimension issues are consolidated.

Mitigation: Check cross-dimension consolidation notes in the generated report and clarify the affected reference before relying on merged priority rankings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laninga/skills/discussion-diagnosis-aggregator)
- [Aggregator Output Template](artifact/references/output-template.md)
- [Aggregator Severity Rubric](artifact/references/severity-rubric.md)
- [Cross-Dimension Map](artifact/references/cross-dimension-map.md)
- [Good Full Diagnosis Example](artifact/references/examples/good_midgley_2020_full_diagnosis.md)
- [Mixed Synthetic Diagnosis Example](artifact/references/examples/mixed_synthetic_partial_issues.md)
- [Bad Synthetic Diagnosis Example](artifact/references/examples/bad_synthetic_full_diagnosis.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown chat response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the conversation language and is self-contained in the assistant reply; final file output occurs only when the user explicitly requests export.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
