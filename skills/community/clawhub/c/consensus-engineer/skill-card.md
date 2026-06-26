## Description: <br>
AI solution architect for consensus-tools that analyzes a project, recommends an integration pattern, scaffolds setup, and proves guard evaluation, consensus voting, persona management, workflow orchestration, and MCP integration work with auditability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide whether consensus-tools fits their AI governance needs, then install and configure guard, wrapper, hybrid, or MCP integrations with project-specific examples and verification output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a project and suggest package-manager commands during setup. <br>
Mitigation: Install it in a version-controlled project and review generated diffs and commands before allowing setup changes. <br>
Risk: Project scanning could expose secrets if environment or key files are read. <br>
Mitigation: Do not allow the skill to read .env or key files; use only configuration patterns and file names for environment discovery. <br>
Risk: MCP, tracing, provider API keys, workflow automation, or cron can add tool access, network side effects, or local state changes. <br>
Mitigation: Enable those capabilities only after reviewing the required access and confirming the intended local or external side effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-engineer) <br>
- [consensus-tools homepage](https://github.com/consensus-tools/consensus-tools) <br>
- [consensus-tools npm organization](https://www.npmjs.com/org/consensus-tools) <br>
- [LangSmith](https://smith.langchain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, ASCII diagrams, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive AskUserQuestion gates; may create or edit project files and run package-manager or TypeScript verification commands when the user approves setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
