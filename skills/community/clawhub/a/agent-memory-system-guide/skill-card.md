## Description: <br>
An agent memory workflow guide for OpenClaw and Codex with MEMORY.md, daily notes, SESSION-STATE, working-buffer, Obsidian archiving, and optional OpenViking support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjke84](https://clawhub.ai/user/cjke84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up a portable, local-first memory workflow with recovery files, daily notes, memory capture, and optional archive or recall layers. It is useful when an agent needs auditable continuity across sessions without depending on a hosted memory platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory files may accidentally contain passwords, API keys, private secrets, or other sensitive workspace information. <br>
Mitigation: Use the workflow for collaboration facts, decisions, and recovery context only; do not store credentials or private secrets in memory files. <br>
Risk: Import or clean restore commands can overwrite supported memory files in the selected workspace. <br>
Mitigation: Confirm the workspace path before running import or --clean and keep the generated pre-import backup for recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjke84/agent-memory-system-guide) <br>
- [Project homepage](https://github.com/cjke84/agent-memory-system-guide) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw memory_search documentation](https://docs.openclaw.ai/tools#memory_search) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory workflow instructions, file templates, and helper-script command examples for an agent workspace.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence and manifest.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
