## Description: <br>
Complete Claude Code productivity system for project setup, prompting patterns, sub-agent orchestration, context management, debugging, refactoring, TDD, and shipping faster without scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill as a Claude Code workflow guide for project setup, prompting, context management, debugging, refactoring, testing, code review, and production shipping checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow guidance can cause an agent to make repository-changing actions such as commits, database changes, or deployments. <br>
Mitigation: Require explicit approval before allowing the agent to commit, change databases, deploy, or perform other repository-changing actions. <br>
Risk: Generated project instructions or handoff files may contain incorrect guidance or expose sensitive context if copied without review. <br>
Mitigation: Review project instructions and handoff files before use, and keep secrets out of persistent context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1kalin/afrexai-claude-code-production) <br>
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only workflow guidance; no executable payload.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
