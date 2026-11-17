## Description:

Designs, reviews, and refactors CLIs for AI agents. Use when building Agent DX CLIs or checking existing CLI contracts. Checks predictability, defense in depth, and context efficiency with evidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to design, review, and refactor command-line interfaces for AI agents. It guides evidence-based checks of CLI contracts and authorized improvements, with scores and unresolved limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security guidance flags possible undisclosed Google Drive metadata queries, and scan coverage was partial.

Mitigation: Before use, review the skill and confirm that Google Drive metadata access fits your workflow.

## Reference(s):

- [Agent DX patterns](references/agent-dx-patterns.md)
- [GWS practice](references/gws.md)
- [SKILL+CLI authoring](references/skill-cli.md)
- [Google Workspace CLI source pinned to commit a3768d0e82ad83cca2da97724e46bea4ff0e6dbd](https://github.com/googleworkspace/cli/tree/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/crates/google-workspace-cli/src)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown report with scored evidence; optional code or CLI changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores are tied to the examined CLI artifact and version; reports include unresolved limits.]

## Skill Version(s):

0.4.3 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
