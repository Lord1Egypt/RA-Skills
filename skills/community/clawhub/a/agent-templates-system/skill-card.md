## Description:

OpenClaw Agent Templates system reference and workflow guide for creating, editing, reviewing, debugging, and extending template-backed agent creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when working on OpenClaw's Agent Templates feature, including template storage, UI editing, gateway handlers, workspace file seeding, identity defaults, and create-from-template flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Template definitions can create or overwrite agent workspace content through workspace files and memory seeds.

Mitigation: Review template definitions before using create-from-template, especially included skills, workspace file modes, and memory seed targets.

Risk: Included skills and partial configuration can change the behavior of agents created from a template.

Mitigation: Inspect included skills, ClawHub URLs, and merged configuration before materializing a template into a real agent.

## Reference(s):

- [Agent Templates Implementation](artifact/references/implementation.md)
- [Agent Template Schema Notes](artifact/references/template-schema.md)
- [Agent Templates UI Design](artifact/references/ui-design.md)
- [Example Agent Template Definition](artifact/assets/examples/agent-template-definition.json)
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/agent-templates-system)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with JSON examples and code reference paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; outputs are intended to guide agent work on OpenClaw template behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
