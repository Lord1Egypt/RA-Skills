## Description:

Generate a GitHub standup summary covering the period since the last standup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone0x](https://clawhub.ai/user/zerone0x)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to summarize their GitHub work for standups, weekly updates, and similar status reports. It gathers merged pull requests and direct commits from a single repository or organization for a selected author and standup cadence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use authenticated GitHub CLI access to inspect repository or organization activity.

Mitigation: Run it only for repositories or organizations whose activity is appropriate to summarize, and prefer repository scope over organization scope when possible.

Risk: Generated summaries can include PR titles and commit messages supplied by repository contributors.

Mitigation: Review the generated standup text before posting or sharing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zerone0x/skills/gh-standup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown standup summary with pull request and direct commit sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes author, repository scope, date range, pull request titles and URLs, commit SHAs, and commit messages.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
