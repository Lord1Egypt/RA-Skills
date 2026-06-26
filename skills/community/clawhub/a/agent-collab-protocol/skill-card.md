## Description: <br>
Standardized agent collaboration protocol for multi-agent systems that defines L0/L1/L2 hierarchy, task contracts, error handling, agent templates, and a new-agent creation checklist for OpenClaw or compatible agent frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[congjianfei](https://clawhub.ai/user/congjianfei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, framework authors, and team leads use this skill to standardize multi-agent collaboration, task handoffs, response formats, and new-agent setup workflows for OpenClaw-compatible systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual deletion instructions could remove OpenClaw workspace or agent directories if copied without review. <br>
Mitigation: Review deletion commands and target paths before executing any operation that removes workspace or agent directories. <br>
Risk: The scaffold script writes under ~/.openclaw using caller-provided domain and role values. <br>
Mitigation: Validate domain names and script arguments before running the scaffold so generated paths stay under intended ~/.openclaw directories. <br>
Risk: The example systemPromptOverride wording may conflict with runtimes that enforce a stricter system, developer, and user instruction priority model. <br>
Mitigation: Replace the example wording before deployment when stricter instruction priority must be preserved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/congjianfei/agent-collab-protocol) <br>
- [Agent Collaboration Protocol](references/AGENT_COLLAB_PROTOCOL.md) <br>
- [Operations Guide](references/OPERATIONS.md) <br>
- [New Agent Checklist](references/NEW_AGENT_CHECKLIST.md) <br>
- [Agent Manual Template](references/TEMPLATE_AGENTS.md) <br>
- [Domain Scaffold Script](references/scaffold-domain.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown protocol documents, reusable templates, shell command examples, and OpenClaw configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an optional shell scaffold that generates domain workspaces under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
