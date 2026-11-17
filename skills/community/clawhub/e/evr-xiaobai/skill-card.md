## Description:

EVR Framework helps agents follow an Execute, Verify, Report workflow so they perform actions, check outcomes, and report evidence instead of claiming unverified completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require agents to execute tasks, verify the result with concrete evidence, and report the outcome clearly. It is most useful for file, command, Git, service, and network tasks where unverified completion claims create operational risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may treat the EVR workflow as permission to run commands with side effects.

Mitigation: Keep normal safeguards for destructive commands, permission changes, services, and network checks, and ask for confirmation when a task has real side effects.

Risk: Verification can give false confidence if the check does not actually prove the requested outcome.

Mitigation: Use task-specific verification evidence, such as file existence, permissions, command exit status, service state, HTTP status, Git status, or a direct content check.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aptratcn/skills/evr-xiaobai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples and reporting templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow guidance; no runtime integration or tool API is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
