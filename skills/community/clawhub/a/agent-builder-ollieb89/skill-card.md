## Description: <br>
Build high-performing, secure OpenClaw agents and multi-agent teams end-to-end. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollieb89](https://clawhub.ai/user/ollieb89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to design or iterate OpenClaw agent workspaces, including workspace files, safety guardrails, orchestration roles, memory practices, and acceptance tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold script writes workspace files and can overwrite similarly named files in the target directory. <br>
Mitigation: Run it only in a new or backed-up directory and review generated workspace files before relying on them. <br>
Risk: Workspace and memory files can expose private preferences, project details, or credentials if sensitive data is added. <br>
Mitigation: Do not store credentials, API keys, private tokens, or unnecessary private details in the workspace or memory files. <br>
Risk: Generated agent rules may not fully match an organization's safety, messaging, or deployment requirements. <br>
Mitigation: Review and tailor the generated guardrails, outbound-message rules, and acceptance tests before deployment. <br>


## Reference(s): <br>
- [OpenClaw Workspace](references/openclaw-workspace.md) <br>
- [Templates](references/templates.md) <br>
- [Architecture](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with fenced file contents and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate OpenClaw workspace files and optional memory logs; review generated files before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
