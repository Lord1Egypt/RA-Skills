## Description:

Generate production-ready code aligned to repo conventions and constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate small-to-medium scoped TypeScript, JavaScript, or Python code from explicit requirements while following the target repository's conventions, validation expectations, and safety constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed trigger metadata may cause the skill to activate outside explicit code-generation requests.

Mitigation: Fix the trigger metadata so activation is limited to explicit code-generation tasks.

Risk: Generated code or validation commands may be incorrect or unsuitable for a repository's conventions.

Mitigation: Review generated code, assumptions, and validation commands before applying or running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-code-generation)
- [Publisher profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with structured summaries, file lists, validation commands, notes, and code or configuration snippets as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify changed files, summarize assumptions or follow-ups, and provide deterministic validation commands.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
