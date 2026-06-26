## Description: <br>
Generates a .ai-context knowledge base that helps coding agents understand a project's purpose, architecture, design decisions, and active issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to generate a .ai-context folder that captures stable project purpose, architecture, design decisions, active issues, and maintenance guidance for future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated project knowledge can be incomplete, stale, or misleading if the agent misses important project context. <br>
Mitigation: Review the generated .ai-context files against the current codebase before relying on them for future agent sessions. <br>
Risk: The Bun helper writes persistent documentation files under .ai-context and may affect existing project context files. <br>
Mitigation: Run it from the intended project root, inspect any existing .ai-context contents first, and use git status or a working branch before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sopaco/ai-context-generator) <br>
- [Writing Guide for AI Context Knowledge Base](references/WRITING-GUIDE.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [Architecture Decision Records](https://adr.github.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent .ai-context documentation that should be reviewed against the current project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
