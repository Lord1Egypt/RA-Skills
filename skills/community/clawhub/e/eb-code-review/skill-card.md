## Description:

Code Review provides multi-agent pull request review that checks for bugs, CLAUDE.md compliance, git history context, and previous PR comments while using confidence scoring to filter false positives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review GitHub pull requests for significant, verifiable issues. It summarizes review findings and can post concise Markdown comments with linked code evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post team-visible GitHub PR comments after broad review-style triggers without an explicit confirmation step.

Mitigation: Use it only when a pull request review comment is intended, and consider requiring confirmation before gh pr comment is run.

## Reference(s):

- [Review Patterns](references/review-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review comments with GitHub links and supporting analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post a team-visible GitHub pull request comment via gh pr comment.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
