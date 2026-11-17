## Description:

Find Skills Clark helps agents discover, compare, and suggest installation of skills, with a China-optimized registry preference and ClawHub fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clark516lian](https://clawhub.ai/user/clark516lian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route skill discovery or installation requests through skill search, compare available skills, and surface install commands with source and risk context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill declares itself high-priority and can steer broad skill-related requests toward skill search and registry-specific installation suggestions.

Mitigation: Review whether this routing behavior is appropriate before installing, and confirm the package source, publisher, version, and risks before approving any installation.

Risk: The security verdict is suspicious because the skill overreaches by making itself mandatory and preferring one registry for some users.

Mitigation: Treat generated search and install commands as proposals; review them before execution and avoid automatic installation without human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clark516lian/skills/find-skills-clark)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes registry source, install command suggestions, and risk context before installation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
