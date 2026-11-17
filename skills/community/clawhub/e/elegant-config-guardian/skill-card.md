## Description:

Safely apply OpenClaw config changes with automatic rollback and ack timeout guard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwu-30](https://clawhub.ai/user/wangwu-30)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to apply risky OpenClaw runtime configuration changes with backup, restart, health-check, and optional manual acknowledgement steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The safety wrapper can run arbitrary shell commands through the supplied apply command.

Mitigation: Review the exact apply command before use, run it without unnecessary privileges, and use only commands from trusted sources.

Risk: Rollback and acknowledgement behavior is weaker than advertised and may require manual recovery.

Mitigation: Keep an independent backup and recovery path for the OpenClaw gateway configuration, and do not treat the ack or rollback flow as the only safety boundary.

## Reference(s):

- [Elegant Config Guardian on ClawHub](https://clawhub.ai/wangwu-30/skills/elegant-config-guardian)
- [wangwu-30 ClawHub profile](https://clawhub.ai/user/wangwu-30)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command guidance for guarded OpenClaw configuration changes; execution depends on the local OpenClaw CLI and the supplied apply command.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
