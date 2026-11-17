## Description:

Smart business-to-dev requirement translator that analyzes a project codebase, understands business requirements, references actual code, and generates implementation-ready development documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wumaohua233](https://clawhub.ai/user/wumaohua233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product engineers, and technical leads use this skill to turn business requirements and optional UI screenshots into implementation-ready development documents grounded in the target codebase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad portions of a project and create a local .ai-memory/project-profile.md summary containing architecture, paths, stack details, and code patterns.

Mitigation: Review the generated project summary in private repositories and add .ai-memory/ to ignore rules if it should not be committed.

Risk: Generated implementation guidance and code references may be incomplete or need adjustment for complex projects.

Mitigation: Have developers review the generated document against the actual codebase before treating it as an execution plan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wumaohua233/skills/business-to-dev-smart)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, implementation references, and structured task lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local .ai-memory/project-profile.md project summary for reuse.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
