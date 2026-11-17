## Description:

AI-powered skill router that analyzes your request and recommends the best installed skill for the job.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viratkumar123](https://clawhub.ai/user/viratkumar123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to find the most relevant installed skill for a natural-language task request. It scans local skill descriptions and returns ranked recommendations with confidence scores and example trigger phrases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads SKILL.md files for locally installed OpenClaw skills and may surface skill names, descriptions, and trigger examples in recommendations.

Mitigation: Install only if local skill metadata disclosure is acceptable, and review recommendations before invoking another skill.

Risk: The matching result is advisory and may recommend an imperfect skill for the user's task.

Mitigation: Use the confidence score and displayed description to choose the next skill manually.

## Reference(s):

- [Capability Match README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/viratkumar123/skills/capability-match)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style text with ranked skill recommendations, confidence scores, and suggested trigger phrases.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are advisory and based on local installed skill metadata.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
