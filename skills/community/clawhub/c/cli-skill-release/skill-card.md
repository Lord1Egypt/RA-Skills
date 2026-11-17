## Description:

Helps developers scaffold, assess, troubleshoot, and publish Python CLI agent skills using release checks, readiness scores, and marketplace guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdhewei](https://clawhub.ai/user/cdhewei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to prepare Python CLI agent skills for distribution, check publication readiness, diagnose release issues, and plan marketplace publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation can execute code from the skill being checked.

Mitigation: Check only trusted repositories and skills, or use a disposable sandbox without sensitive environment variables; avoid inventory and recheck over unknown skills.

Risk: The ClawHub dry-run publish path can still call the publisher.

Mitigation: Do not rely on publish --clawhub --dry-run to prevent publication until the path is fixed.

Risk: Release and publication can change files or publish unintended content.

Mitigation: Review diffs and publication targets before releasing or publishing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cdhewei/skills/cli-skill-release)
- [Server-resolved source repository](https://github.com/cdhewei/cli-skill-release)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Readiness scores and release checklists may be included.]

## Skill Version(s):

1.9.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
