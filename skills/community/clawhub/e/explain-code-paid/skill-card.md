## Description:

代码 explains code with visual diagrams and analogies, with paid-release claims for static analysis, dependency issue detection, batch code review, CI/CD integration, complexity visualization, and refactoring suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand code snippets, teach codebase structure, explain functions or classes, and receive code review or improvement guidance. It is not intended for non-code concept explanation or general knowledge Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release as suspicious because it asks for command execution and file-writing authority while the core use case is code explanation.

Mitigation: Review the skill carefully before installation, run it in a constrained workspace, and require explicit user approval before executing commands or writing files.

Risk: The skill description includes broad code generation, review, testing, deployment, and batch-processing behavior beyond simple explanation.

Mitigation: Limit use to explanation and review workflows unless the user has verified that broader automation behavior is appropriate for the project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/explain-code-paid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-style structured responses, with possible inline code, shell commands, configuration snippets, diagrams, and review findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include summaries, scores, findings, prioritized improvement suggestions, architecture explanations, flow diagrams, and dependency relationships.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
