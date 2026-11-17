## Description: <br>
Agent Copilot Pro helps AI agent developers design structured prompts, decompose tasks, choose tools, manage context decay, evaluate hallucination risk, and define agent-loop workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent engineers use this skill to create and review prompts, task-decomposition plans, tool-selection policies, context-management practices, output schemas, and quality checks for AI agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares exec capability and may lead an agent to propose command execution for validation tasks. <br>
Mitigation: Treat exec as optional authority and review any proposed command before allowing execution. <br>
Risk: Prompt-engineering, tool-selection, and task-decomposition guidance can still produce incorrect or misleading recommendations. <br>
Mitigation: Review generated prompts, schemas, tool plans, and task plans before deployment, and use the skill's quality checks and regression tests for higher-risk workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agent-copilot-pro) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, schemas, and code or shell snippets when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured prompt templates, DAG task plans, tool-selection recommendations, context-governance advice, validation schemas, and regression-test cases.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
