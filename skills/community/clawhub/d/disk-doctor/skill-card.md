## Description:

Diagnose and safely reclaim disk space on an OpenClaw host

This skill is ready for commercial/non-commercial use.

## Publisher:

[breakzoras](https://clawhub.ai/user/breakzoras)

### License/Terms of Use:

MIT-0

## Use Case:

Operators of OpenClaw hosts use this skill to identify disk usage and consider cache cleanup or other space recovery steps. It emphasizes preserving user data and getting explicit approval before removing Docker resources or other large items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reports host uptime and CPU-ranked processes, which the security review says do not match its stated disk diagnosis and cleanup purpose.

Mitigation: Before use, consider whether those host and process reports are useful; review the commands and share their output only with the intended recipient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/breakzoras/skills/disk-doctor)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostic steps, cleanup guidance, and approval requests for potentially destructive actions.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
