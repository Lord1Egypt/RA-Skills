## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwang-wh](https://clawhub.ai/user/williamwang-wh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to vet ClawHub, GitHub, or other sourced skills before installation by checking source trust, required permissions, red flags, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested repository lookup commands may query public GitHub information for candidate skills.

Mitigation: Run commands only against intended public repositories and review command targets before execution.

Risk: Checklist results can be misleading if treated as a complete security audit.

Mitigation: Use the report as pre-install screening and require human review for high-risk findings, credential access, or system-level behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwang-wh/skills/claw-skill-vetter-pro)
- [Publisher profile](https://clawhub.ai/user/williamwang-wh)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown report with checklist guidance and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewable security vetting notes; does not request credentials, root access, persistence, or hidden system changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
