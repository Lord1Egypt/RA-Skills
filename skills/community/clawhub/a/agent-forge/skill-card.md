## Description: <br>
Agent Forge creates independent OpenClaw agents through an interview that gathers role, model, channel, tool, sandbox, and personality requirements, then scaffolds agent files and updates multi-agent configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limoxt](https://clawhub.ai/user/limoxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to create dedicated agents with isolated workspaces, generated operating documents, configured tool and channel access, and updated multi-agent communication settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent OpenClaw agents and modify multi-agent communication settings. <br>
Mitigation: Use it only when those persistent changes are intended, review generated files and gateway patches before deployment, and keep session visibility and tool access as narrow as practical. <br>
Risk: Broad trigger phrases combined with no clear final approval gate could cause unexpected agent or configuration changes. <br>
Mitigation: Require explicit user confirmation after the interview and before running deployment scripts or applying gateway configuration updates. <br>
Risk: Copied USER.md content may expose sensitive user context to newly created agent workspaces. <br>
Mitigation: Review USER.md before copying it and use simple, trusted agent IDs with limited workspace and tool permissions. <br>


## Reference(s): <br>
- [Agent Forge Skill Page](https://clawhub.ai/limoxt/agent-forge) <br>
- [OpenClaw Multi-Agent Architecture](references/openclaw-multi-agent.md) <br>
- [Agent Forge API Reference](references/api_reference.md) <br>
- [OpenClaw Multi-Agent Concepts](https://docs.openclaw.ai/concepts/multi-agent) <br>
- [OpenClaw Session Concepts](https://docs.openclaw.ai/concepts/session) <br>
- [OpenClaw Subagents Tool](https://docs.openclaw.ai/tools/subagents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Interview-driven Markdown files, JSON configuration, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent OpenClaw workspace files and proposes or applies multi-agent gateway settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
