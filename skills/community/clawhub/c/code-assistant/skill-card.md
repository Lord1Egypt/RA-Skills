## Description:

Asistente de programación especializado. Analiza código, encuentra bugs, sugiere optimizaciones, refactoriza y genera documentación automáticamente.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miguelguerra200022-sudo](https://clawhub.ai/user/miguelguerra200022-sudo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect local source files for heuristic bug, security, complexity, documentation, and optimization signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation claims broad refactoring, testing, agent delegation, and self-repair capabilities that are broader than the local analyzer behavior evidenced in the artifact.

Mitigation: Review supported commands and treat unsupported automation claims as unverified before relying on them.

Risk: The analyzer reports heuristic bug and security findings that may be incomplete or false positive.

Mitigation: Use findings as review leads and validate them against the source code before making changes.

Risk: Future auto-fix or refactor behavior could change files if added later.

Mitigation: Run the skill on projects under version control and require explicit review before accepting generated changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miguelguerra200022-sudo/skills/code-assistant)
- [Publisher Profile](https://clawhub.ai/user/miguelguerra200022-sudo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and console-style text with code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces heuristic analysis and generated documentation text; findings should be reviewed before acting on them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
