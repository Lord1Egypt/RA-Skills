## Description: <br>
Code Dev Toolkit Free guides individual developers through a five-step request, plan, execute, verify, and deliver coding workflow with optional local preference memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual engineers use this skill to plan, implement, verify, test, and deliver coding tasks in small reviewable steps. It is suited to personal project work, refactoring, technical planning, and validation checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an assistant to read project files and run local development commands when the user asks. <br>
Mitigation: Review proposed commands before execution and run them only in trusted project workspaces. <br>
Risk: Preference memory in ~/code/memory.md could store sensitive information if a user asks the assistant to remember it. <br>
Mitigation: Do not store secrets, credentials, tokens, or sensitive project details in preference memory. <br>
Risk: Generated plans, code changes, or validation advice may be incomplete or incorrect for a specific codebase. <br>
Mitigation: Validate each step with targeted tests, review code changes, and run the full relevant test suite before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/code-dev-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists, examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose project-specific commands and local preference updates only when the user asks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
