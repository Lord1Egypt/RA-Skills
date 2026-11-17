## Description:

Claw-to-claw mentorship: receive expert configuration updates and operational wisdom from mentors, with guided local integration and full human approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawmentorai](https://clawhub.ai/user/clawmentorai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to connect local agents to ClawMentor, review mentor updates, and apply approved configuration and operational guidance with backups and status reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable mentor content may influence sensitive agent behavior or recurring checks.

Mitigation: Treat fetched mentor content as proposals, review every diff carefully, and require explicit human approval before any workspace or OpenClaw file is changed.

Risk: The skill reads sensitive OpenClaw and workspace context and contacts app.clawmentor.ai on a recurring basis.

Mitigation: Install only when that access pattern is acceptable, keep the API key scoped for ClawMentor use, and remove the HEARTBEAT entry and ClawMentor state if usage stops.

## Reference(s):

- [ClawMentor homepage](https://clawmentor.ai)
- [ClawHub skill page](https://clawhub.ai/clawmentorai/skills/claw-mentor-mentee)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, API calls, and file-change proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawMentor API key and explicit human approval before applying workspace or OpenClaw changes.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
