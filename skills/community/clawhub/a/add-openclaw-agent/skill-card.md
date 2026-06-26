## Description: <br>
Create a new OpenClaw agent via exec (openclaw agents add) and configure its identity + operating rules by editing the new workspace files (IDENTITY.md, AGENTS.md). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiguazhiPrince](https://clawhub.ai/user/xiguazhiPrince) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create an isolated OpenClaw agent, configure its identity, and append role-specific operating rules based on the user's requested purpose and constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide creation of a persistent OpenClaw agent and workspace. <br>
Mitigation: Review the agent name, workspace path, optional bind/model flags, and the proposed command before confirming execution. <br>
Risk: Workspace edits could change identity or operating rules in ways the user did not intend. <br>
Mitigation: Review the appended IDENTITY.md and AGENTS.md content and keep default template text intact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiguazhiPrince/add-openclaw-agent) <br>
- [Multi-Agent Routing](/concepts/multi-agent) <br>
- [Agent workspace](/concepts/agent-workspace) <br>
- [OpenClaw agents CLI](/cli/agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file-editing instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before agent creation and focuses configuration changes on IDENTITY.md and AGENTS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
