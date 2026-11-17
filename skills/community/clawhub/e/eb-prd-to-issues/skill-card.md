## Description:

Breaks a PRD into independently grabbable GitHub issues using tracer-bullet vertical slices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn a PRD GitHub issue into reviewed, dependency-ordered implementation issues that deliver thin vertical slices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read GitHub issue contents from private or sensitive repositories.

Mitigation: Confirm the repository and PRD issue before fetching issue content.

Risk: The skill may create GitHub issues with incorrect scope, dependencies, or sensitive text.

Mitigation: Review the proposed breakdown and drafted issue text before allowing issue creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emersonbraun/skills/eb-prd-to-issues)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown issue breakdowns and GitHub issue bodies with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review of the proposed issue breakdown before issue creation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
