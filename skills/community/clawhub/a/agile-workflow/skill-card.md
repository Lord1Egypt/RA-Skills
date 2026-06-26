## Description: <br>
Agile Workflow is an automated multi-agent workflow engine for task decomposition, dependency management, monitoring, repair, and coordinated execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XBCS](https://clawhub.ai/user/XBCS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to coordinate OpenClaw agents across writing, software development, documentation, analysis, and other multi-step tasks. It decomposes work, tracks dependencies and task state, monitors agent activity, and emits commands or configuration guidance for operating the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that the skill can start, stop, restart, and repair local agents with limited user confirmation. <br>
Mitigation: Install and run it only in a dedicated OpenClaw workspace where this level of background automation is acceptable. <br>
Risk: The security guidance flags background monitors, process inspection or termination, local logging and caching, gateway restart behavior, cron/nohup usage, and hard-coded paths as review areas. <br>
Mitigation: Review cron and nohup instructions, health-check repair behavior, cleanup scripts, and hard-coded paths before enabling the skill in shared or sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/XBCS/agile-workflow) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [v7.0 Usage Guide](artifact/docs/v7.0-使用指南.md) <br>
- [v7.0 Concurrent Safety Architecture](artifact/docs/ADD-v7.0-并发安全架构.md) <br>
- [v7.18 Token Limit Fix](artifact/docs/ADD-v7.18-Token 超限修复.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with command examples, JSON configuration snippets, and JavaScript usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local workflow status, health-check, repair, cleanup, and monitoring guidance for OpenClaw workspaces.] <br>

## Skill Version(s): <br>
7.18.1 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
