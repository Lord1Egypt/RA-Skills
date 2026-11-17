## Description:

Interprets physical exam reports from uploaded images, PDFs, or pasted text by explaining lab indicators, reference ranges, abnormal values, and follow-up suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marson2016](https://clawhub.ai/user/marson2016)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to understand physical exam and lab reports, including blood panels, liver function, lipids, kidney function, urinalysis, tumor markers, and historical comparisons. It provides plain-language explanations and flags abnormal values while avoiding diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded medical reports may contain sensitive personal health information.

Mitigation: Redact unnecessary identifiers when possible before using the skill.

Risk: Medical explanations of abnormal values could be mistaken for a diagnosis.

Mitigation: Treat the output as explanatory guidance, rely on the report's own reference ranges first, and consult a clinician for significant abnormalities or follow-up decisions.

## Reference(s):

- [Common physical exam indicator reference ranges](references/ranges.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with summary tables and plain-language recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes the report's own reference ranges before bundled reference ranges; output is explanatory guidance, not a diagnosis.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
