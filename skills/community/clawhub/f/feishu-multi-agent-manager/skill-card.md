## Description:

Guides users through configuring a Feishu-based multi-agent OpenClaw system with batch agent creation, credential checks, role templates, and configuration backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create and configure multiple Feishu bot-backed agents, assign role templates, validate App ID/App Secret formats, update OpenClaw configuration, and generate per-agent workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secrets are sensitive and are stored in OpenClaw configuration.

Mitigation: Use only in a trusted local OpenClaw environment, keep openclaw.json private, and rotate Feishu credentials regularly.

Risk: Batch creation writes persistent OpenClaw configuration and per-agent SOUL.md, AGENTS.md, and USER.md files.

Mitigation: Review generated files and the automatic backup before restarting OpenClaw.

Risk: Custom agent IDs or names can affect generated paths and persona text if they contain path characters, newlines, or instructions.

Mitigation: Restrict custom agent IDs and names to simple safe values before running batch creation.

Risk: Dependencies installed through npx may change over time.

Mitigation: Pin npx-installed dependencies in the deployment environment before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/skills/feishu-multi-agent-manager)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Multi-Agent Routing Documentation](https://clawd.org.cn/concepts/multi-agent.html)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with TypeScript API examples, bash commands, and generated OpenClaw configuration/workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes OpenClaw config and per-agent workspace/persona files during batch creation.]

## Skill Version(s):

2.0.5 (source: server release metadata and skill.json; source files also contain 2.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
