## Description:

Perform multi-dimensional advanced code analysis including knowledge graph generation, code quality evaluation, performance analysis, security review, architecture review, and test coverage analysis, outputting structured reports with actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze codebases for code review, quality, performance, security, architecture, and test coverage findings, then produce prioritized recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate broadly for ordinary code-review or security-review prompts and inspect private or unrelated code if scope is unclear.

Mitigation: Give explicit file or directory scope before use, especially in workspaces containing private or unrelated code.

Risk: Code-analysis recommendations may be incomplete or need project-specific review before implementation.

Mitigation: Review findings and proposed changes against repository requirements before applying them.

## Reference(s):

- [Code Analysis Skill Page](https://clawhub.ai/openlark/skills/code-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with findings, risk assessment, improvement roadmap, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized recommendations and risk levels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
