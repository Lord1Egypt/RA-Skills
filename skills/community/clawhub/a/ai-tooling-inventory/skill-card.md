## Description:

Builds a healthcare AI capability inventory across purchases, in-house builds, vendor AI features, integrations, and free tools, then classifies ePHI contact, agreement coverage, ownership, verification, and risk-analysis scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dangsllc](https://clawhub.ai/user/dangsllc)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare compliance, privacy, security, and operations staff use this skill to identify AI-enabled tools operating on organizational work product and to produce structured inventory rows, findings, recommendations, and coverage statements for HIPAA risk-analysis scoping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may surface sensitive organizational metadata about AI use, OAuth grants, browser extensions, and vendor AI features.

Mitigation: Use it with an appropriate organizational respondent and handle the resulting inventory and findings as sensitive compliance material.

Risk: Users may provide patient records when describing AI workflows.

Mitigation: Avoid patient records and provide system-level metadata, artifact names, tool behavior, scopes, and interview answers instead.

Risk: Findings can raise breach or BAA adequacy questions that require legal judgment.

Mitigation: Treat breach determination and BAA adequacy as matters for qualified legal or regulatory counsel.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dangsllc/skills/ai-tooling-inventory)
- [Interview Question Bank](references/interview-questions.md)
- [Vendor AI Feature Inquiry Letter Template](references/vendor-letter.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON-style inventory and finding objects, recommendations, and coverage statements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional vendor inquiry letter text only when the user asks for it]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter reports 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
