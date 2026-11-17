## Description:

Turn GitHub Issues into a local agent queue. GitHub issues in, agent work out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikil511](https://clawhub.ai/user/nikil511)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to operate GitHub Issues and Project Boards as a local, git-backed work queue for agent tasks and deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide ClawQueue operation over GitHub issues, project boards, and local repositories.

Mitigation: Install and run it only for repositories and boards where agent scheduling is intended, and review workflow policy before scheduler or retry commands are used.

Risk: Private profile configuration can contain GitHub and LLM credentials.

Mitigation: Keep clawqueue.private.json private and limit tokens to the minimum scopes required for the configured workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikil511/skills/clawqueue)
- [ClawQueue core repository](https://github.com/ClawQueue/ClawQueue)
- [ClawQueue GitHub organization](https://github.com/ClawQueue)
- [ClawQueue reports repository](https://github.com/ClawQueue/ClawQueue-reports)
- [ClawQueue documentation](https://clawqueue.github.io/ClawQueue/)
- [openclaw-balena repository](https://github.com/ClawQueue/openclaw-balena)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and git; may reference local ClawQueue profiles, worklog repositories, service logs, scheduler state, and private credential configuration.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
