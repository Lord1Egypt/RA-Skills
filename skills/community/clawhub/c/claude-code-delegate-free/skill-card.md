## Description:

代码委派基础版 helps developers delegate programming tasks to an AI assistant for task breakdown, code generation, basic validation, and execution logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn a natural-language programming task into smaller implementation steps, generated code or documentation, and a brief execution log. It is intended for routine code generation, completion, simple refactoring, debugging, testing, and deployment assistance when the technical stack is clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read project files and run local commands during coding workflows.

Mitigation: Review proposed commands before execution, avoid exposing secrets, and use the skill in a project or sandbox where code-generation and test commands are expected.

Risk: Generated code or refactoring suggestions may be incomplete, incorrect, or unsuitable for complex architecture decisions.

Mitigation: Review generated code before use, run project tests and static checks, and split complex work into smaller tasks with clear technical requirements.

Risk: Project context may contain credentials, tokens, or other sensitive data.

Mitigation: Do not provide secrets as task input and keep credentials in protected environment variables or secret stores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/claude-code-delegate-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown, code snippets, structured JSON-style results, and execution-log summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include generated code, language metadata, line counts, step status, timing information, and error details.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
