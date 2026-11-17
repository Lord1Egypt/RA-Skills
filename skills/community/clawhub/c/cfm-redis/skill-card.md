## Description:

CFM Redis provides Redis Pub/Sub based real-time communication between agent frameworks with event-driven messaging and reduced polling-related token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ameylover](https://clawhub.ai/user/ameylover)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up Redis-backed messaging, history, discovery, and command-line workflows for multi-agent collaboration across frameworks such as Hermes and OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Redis messages and history can expose sensitive content if users send secrets or connect to an untrusted Redis instance.

Mitigation: Use only a trusted local or properly secured Redis instance and do not send secrets through the messaging channel.

Risk: Cron, daemon, file-trigger, and webhook modes can repeatedly process, forward, or persist messages without adequate controls.

Mitigation: Enable these modes only after Redis authentication, retention limits, sender verification, path validation, and outbound destination controls are in place.

Risk: The artifact includes approval-bypass guidance that could encourage unsafe execution practices.

Mitigation: Remove the approval-bypass instruction before installation or release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ameylover/skills/cfm-redis)
- [Project homepage](https://github.com/AmeyLover/cfm-redis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires redis-server, python3, and the Python redis package.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
