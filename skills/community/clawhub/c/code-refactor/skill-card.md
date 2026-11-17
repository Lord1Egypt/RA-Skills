## Description:

Improves readability, structure, and maintainability of a local codebase while preserving behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sf0799](https://clawhub.ai/user/sf0799)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to clean up naming, reduce duplication, simplify control flow, and reorganize code without changing public behavior or compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated refactoring can unintentionally change behavior or compatibility.

Mitigation: Review diffs, preserve public interfaces unless explicitly allowed, and run the existing test or validation path after changes.

Risk: The skill can modify local code during refactoring.

Mitigation: Use it in a reviewable workspace and inspect proposed edits before accepting or shipping them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sf0799/skills/code-refactor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown summaries with code changes or command snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on behavior-preserving refactoring, rationale, and validation notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
