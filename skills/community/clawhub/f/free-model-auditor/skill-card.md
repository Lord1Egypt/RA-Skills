## Description:

Audits WorkBuddy's free-model registry across providers, tests candidates for availability and repeated-request usability, and applies supported additions and removals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igenomed](https://clawhub.ai/user/igenomed)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and administrators use this skill to check configured providers for usable free chat models, update their model registry, and receive an audit report.

### Deployment Geography for Use:

Global, subject to provider availability and network access

## Known Risks and Mitigations:

Risk: The audit reads API keys stored in models.json and sends authenticated requests to external model providers.

Mitigation: Use scoped, rotatable provider keys and review the providers and network or proxy configuration before running.

Risk: Registry edits could add incorrect models or remove wanted entries.

Mitigation: Run the dry-run first, review the add/remove diff, and retain the generated models.json backup.

Risk: Live model tests may consume quota or encounter rate limits and network restrictions.

Mitigation: Expect test traffic and rate limits; defer decisions about unreachable providers until network access is restored.

## Reference(s):

- [Free Model Auditor on ClawHub](https://clawhub.ai/igenomed/skills/free-model-auditor)
- [Provider audit policies](artifact/references/platforms.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration]

**Output Format:** [Markdown audit report and updated models.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a full model inventory and an add/remove diff; registry changes require a WorkBuddy restart.]

## Skill Version(s):

1.7.1 (source: SKILL.md frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
