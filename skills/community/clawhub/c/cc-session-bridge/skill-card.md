## Description:

Installs and uses a Claude Code to OpenClaw session bridge that converts Claude Code stream output into OpenClaw session records so AIMA can collect and display them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steflerjiang](https://clawhub.ai/user/steflerjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and run a bridge that makes Claude Code sessions visible in AIMA/OpenClaw workflows, including task binding and appending subsequent runs to existing session records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge persistently records and shares detailed session data, including prompts, tool outputs, file-derived content, and metadata.

Mitigation: Use only in approved workspaces, set the narrowest practical --cwd, avoid sensitive directories, and confirm that task viewers are allowed to see the resulting session records.

Risk: The supplied sender and task metadata should not be treated as verified identity or authorization.

Mitigation: Restrict AIMA CLI credentials, validate task IDs and identity metadata through trusted controls, and review records before relying on them for attribution.

Risk: Detailed Claude Code events and tool results can expose sensitive local context through generated session records.

Mitigation: Review generated records for sensitive content before sharing, redact secrets when needed, and run the bridge with least-privileged workspace access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steflerjiang/skills/cc-session-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation and runtime use of a local bridge script that emits JSONL session records.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
