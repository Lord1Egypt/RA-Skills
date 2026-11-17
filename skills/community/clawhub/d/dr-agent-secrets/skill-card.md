## Description:

Persistent local secret setup, rotation, inspection, and recovery with SecretRefs, protected env fragments, redaction, and restart safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-refahi-ikara](https://clawhub.ai/user/daniel-refahi-ikara)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up, inspect, rotate, and recover persistent credentials for OpenClaw agents while keeping secret values out of durable text and checking that services can use them safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential values or sensitive diagnostics could be exposed, and changes to persistent service settings could disrupt existing consumers.

Mitigation: Keep secret values out of chat and durable records, report key names and presence only, preserve unrelated service settings and files, follow the documented permission and approval safeguards, and review dr-runtime-contract separately before using it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daniel-refahi-ikara/skills/dr-agent-secrets)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Redacted status summaries]

**Output Format:** [Markdown guidance with shell commands, configuration steps, and redacted validation receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret values are excluded; reports contain paths, key names, permissions, and validation status only.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
