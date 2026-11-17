## Description:

EvoMap WorkBench v1.0.11 Mini helps agents work with EvoMap AI decision evolution, knowledge graph search, predictive maintenance, adaptive learning, and decision tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesimagine-oss](https://clawhub.ai/user/yesimagine-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to experiment with EvoMap decision workflows, asset validation, network-aware retries, task recovery, and optional Feishu or notification status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse local OpenClaw Feishu credential or configuration files and send data externally.

Mitigation: Review credential sources, recipients, transmitted fields, and outbound notification or validation traffic before installation; prefer isolated or non-production credentials.

Risk: Install and uninstall flows can read or modify local OpenClaw configuration.

Mitigation: Back up OpenClaw configuration and test install or uninstall behavior in a disposable environment before using it in a shared workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesimagine-oss/skills/evomap-workbench-min)
- [ClawHub publisher profile](https://clawhub.ai/user/yesimagine-oss)
- [EvoMap A2A validation endpoint](https://evomap.ai/a2a/validate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON or configuration output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, operational status, and generated JSON reports.]

## Skill Version(s):

1.0.11 (source: server evidence release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
