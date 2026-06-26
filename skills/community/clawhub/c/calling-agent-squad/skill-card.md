## Description: <br>
Activate a multi-agent team to manage complex projects, business tasks, or development workflows with specialized roles and quality control loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbiger](https://clawhub.ai/user/arbiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and project owners use this skill to coordinate a role-based agent squad for project planning, research, writing, implementation, review, and mission logging. It supports a standard single-agent role sequence and a full mode that initializes and invokes separate OpenClaw sub-agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sub-agents and bundled role instructions can create files, invoke tools, and coordinate work beyond a single response. <br>
Mitigation: Install only after review, run in a constrained workspace, and require explicit approval before enabling full mode or spawning separate agents. <br>
Risk: Generic AGENTS.md instructions include personal-assistant behaviors, memory maintenance, communication guidance, and repository publishing behaviors that are broader than the squad workflow. <br>
Mitigation: Disable or rewrite heartbeat, personal-service, group-chat, memory, and commit/push sections before deployment unless those behaviors are intentionally required. <br>
Risk: The skill can create local project folders and persistent markdown documentation. <br>
Mitigation: Review generated project paths, keep outputs in a dedicated workspace, and inspect created files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arbiger/calling-agent-squad) <br>
- [Publisher Profile](https://clawhub.ai/user/arbiger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands, generated project files, and agent configuration instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project folders under Documents/squad_projects, write mission documentation, and in full mode invoke OpenClaw sub-agents in separate workspaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
