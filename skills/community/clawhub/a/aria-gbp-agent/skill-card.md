## Description:

Agent identity package for Aria that installs SOUL.md, IDENTITY.md, and AGENTS.md into an OpenClaw workspace to give an AI agent its Google Business Profile specialist identity, personality, and operating rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

External developers or operators use this package when setting up or replacing an OpenClaw agent identity for Aria, a Google Business Profile specialist intended to help a marketing agency owner manage, audit, and optimize multiple business profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package persistently replaces workspace identity and operating rules.

Mitigation: Back up existing SOUL.md, IDENTITY.md, AGENTS.md, BOOTSTRAP.md, MEMORY.md, and memory notes before copying the package files.

Risk: The workspace rules enable broad private-context loading and memory updates.

Mitigation: Review and narrow memory-loading, memory-writing, and group-chat rules before deployment, especially for shared or multi-user contexts.

Risk: The setup rules allow deletion of BOOTSTRAP.md after first use.

Mitigation: Require human review before deleting setup files or remove that behavior from the installed rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/aria-gbp-agent)
- [ClawHub Publisher Profile](https://clawhub.ai/user/maverick-software)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown identity files and Markdown installation guidance with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent workspace identity and operating-rule files for an OpenClaw agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
