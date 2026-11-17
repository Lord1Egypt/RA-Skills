## Description:

Use when turning approved plans, specs, PRDs, or Epics into trackable GitHub Issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to turn approved roadmaps and specifications into linked GitHub Issues and keep Epic tracking consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change Issues, labels, and planning links in the authenticated GitHub repository.

Mitigation: Confirm the target repository and review proposed changes before allowing publication or edits.

Risk: Canonical labels and the Portuguese blocker-comment convention may not fit an existing team's workflow.

Mitigation: Confirm the label set and comment convention with the team before using the skill on an active repository.

## Reference(s):

- [Create Issues on ClawHub](https://clawhub.ai/afonsoft/skills/create-issues)
- [Publisher-listed skills repository](https://github.com/afonsoft/skills)
- [GitHub CLI manual](https://cli.github.com/manual/)
- [SPEC SDD issue template](references/spec-sdd-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with GitHub CLI commands and issue templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update GitHub Issues, labels, and roadmap links using the authenticated GitHub CLI.]

## Skill Version(s):

1.0.10 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
