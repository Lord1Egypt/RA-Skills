## Description: <br>
Agency Agents is a prompt-only AI agent team skill for single-agent tasks, department workflows, and multi-agent orchestration across product, engineering, marketing, testing, and support roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, founders, and operators use this skill to invoke specialized agent personas for application development, marketing planning, product and project management, testing, and coordinated multi-agent project work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release claims a broad 61-agent package, while server security evidence says the included prompt package overstates what is included. <br>
Mitigation: Treat unavailable or unimplemented personas as unavailable, and inspect the installed files before relying on a claimed department or agent. <br>
Risk: The orchestrator asks for broad autonomous project execution and may persist local outputs with limited disclosure. <br>
Mitigation: Require explicit checkpoints and file-write approval before execution, and inspect or delete the ~/clawd/agency-agents output folder after use. <br>
Risk: Prompt-only agent workflows may receive sensitive business, customer, or codebase data. <br>
Mitigation: Avoid placing secrets or sensitive customer data in prompts, and redact confidential context before sharing tasks with the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jerry-guo-mys/agency-agents) <br>
- [Publisher Profile](https://clawhub.ai/user/jerry-guo-mys) <br>
- [Quickstart](docs/QUICKSTART.md) <br>
- [Project Summary](PROJECT_SUMMARY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell-command, configuration, and project-report examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only outputs; selected agent personas may propose implementation snippets, plans, file changes, commands, or review findings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata); 1.0.0 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
