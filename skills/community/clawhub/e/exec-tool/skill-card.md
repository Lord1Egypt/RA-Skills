## Description:

Exec Tool runs approved ClawHub CLI commands in controlled OpenClaw workflows and returns trimmed command output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayuran1096](https://clawhub.ai/user/mayuran1096)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to trigger ClawHub CLI tasks for automation, debugging, chat-based system management, and controlled VPS workflows. It should be installed only where command execution is tightly sandboxed and minimally privileged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command-execution boundary is ineffective and may allow arbitrary shell commands despite claimed destructive-command protections.

Mitigation: Review before installing; use only in a tightly sandboxed environment with a minimally privileged account, and replace raw shell-string execution with structured ClawHub subcommand validation using shell=False before exposing it to agents, chat, webhooks, or untrusted input.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mayuran1096/skills/exec-tool)
- [Publisher Profile](https://clawhub.ai/user/mayuran1096)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output is truncated to 4,000 characters.]

## Skill Version(s):

1.0.0 (source: release evidence, skill.yaml, clawdis.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
