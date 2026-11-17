## Description:

Accesses a local Dessix desktop workspace through a Node.js bridge client so an agent can read, search, invoke Dessix tools, build local automations, and fetch Action or Scene prompt content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiangst0816](https://clawhub.ai/user/xiangst0816)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect to a trusted local Dessix desktop app, inspect workspace content, invoke Dessix tools, and automate creation or maintenance of Action, Scene, workspace, and block records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad bridge access can let an agent read or change Dessix workspace content.

Mitigation: Use only with a trusted Dessix desktop app, run read-only workflows first, and approve exact bridge tool names plus block or workspace IDs before create, update, delete, or restore operations.

Risk: Mutable npx or global npm installation examples can resolve changing package contents over time.

Mitigation: Prefer pinned installation commands or a reviewed local checkout for deployments that need repeatable behavior.

## Reference(s):

- [Dessix Tool Quick Reference](references/dessix-tools.md)
- [Dessix Skill Homepage](https://github.com/DessixIO/skill)
- [Dessix / ClawHub Project](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON argument templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a running trusted Dessix desktop app; bridge endpoint may be configured with DESSIX_MCP_BRIDGE_ENDPOINT.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
