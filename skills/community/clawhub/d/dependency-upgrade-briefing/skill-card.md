## Description:

Creates Chinese-language dependency upgrade briefings that summarize upgrade benefits, risks, rollback plans, business impact, and recommended timing from user-supplied upgrade details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn dependency names, version changes, and changelog summaries into review-ready upgrade briefings. It is suited for upgrade review, technical debt planning, and release communication where missing facts should be called out instead of invented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings can be incomplete or misleading if the input omits dependency names, version changes, or changelog summaries.

Mitigation: Provide concrete upgrade details and review the generated pending-confirmation items before using the briefing for planning or release communication.

Risk: Sensitive dependency or business context could be included in generated local output files.

Mitigation: Remove sensitive details before processing and choose an intended local path when using --output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/dependency-upgrade-briefing)
- [README](artifact/README.md)
- [Structured output spec](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown briefing, with optional JSON wrapper when the bundled script is run with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated briefing to a user-selected local output path when --output is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
