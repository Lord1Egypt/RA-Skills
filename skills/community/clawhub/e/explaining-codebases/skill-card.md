## Description:

Use when creating an interactive explainer about a codebase, repository, or source files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[analyticalmonk](https://clawhub.ai/user/analyticalmonk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn real repository code into interactive explainers for onboarding, architecture overviews, and focused implementation deep-dives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to inspect repository files, which may include private code or secrets.

Mitigation: Use it only on repositories whose contents are appropriate for agent analysis, and avoid repositories containing secrets or private code you do not want analyzed.

Risk: Implicit invocation can cause the skill to run when an environment auto-loads matching skills.

Mitigation: Review skill activation settings before installation in environments where implicit invocation is enabled.

Risk: Codebase explainers can become inaccurate if snippets or claims drift from the current implementation.

Mitigation: Run the required fact-checking step against exact source paths and line numbers before delivery.

## Reference(s):

- [Code Intake](artifact/references/code-intake.md)
- [Code-Specific Figure Archetypes](artifact/references/code-figure-archetypes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance for a self-contained interactive explainer with anchored code snippets and figure plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fact-checking against the source code before delivery.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
