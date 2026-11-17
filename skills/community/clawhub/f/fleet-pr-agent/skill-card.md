## Description:

Multi-repo PR monitoring and triage agent. Scans GitHub repos for open PRs, prioritizes by staleness/review status/CI state, and generates a structured Markdown triage summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanxevo3](https://clawhub.ai/user/lanxevo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scan open pull requests across one or more GitHub repositories, rank them by urgency, and produce a concise triage report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included Bash helper has a command-execution weakness if run with attacker-controlled environment variables.

Mitigation: Prefer the documented Python script and require integer validation for FLEET_PR_STALE_DAYS, FLEET_PR_CI_WEIGHT, and FLEET_PR_MAX_PRS before using the Bash helper.

Risk: The skill uses the authenticated GitHub CLI to read pull request metadata from repositories available to the user's token.

Mitigation: Run it with a least-privilege GitHub token and review generated triage reports before taking repository actions.

## Reference(s):

- [Fleet PR Agent on ClawHub](https://clawhub.ai/lanxevo3/skills/fleet-pr-agent)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown triage report with prioritized PR lists and a summary section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated GitHub CLI access and repository visibility through the user's GitHub token.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
