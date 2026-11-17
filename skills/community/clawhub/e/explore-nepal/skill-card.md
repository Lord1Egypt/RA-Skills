## Description:

Book flights to Nepal including Kathmandu and Pokhara, with support for related travel planning tasks powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search Nepal-related flight options, compare routes by price, duration, or directness, and present provider booking links from flyai CLI results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm CLI before use.

Mitigation: Require explicit user approval before installation and review or pin the CLI package version in controlled environments.

Risk: The skill runs shell commands using user-derived travel parameters.

Mitigation: Validate origin, destination, and date fields before execution, and reject unusual punctuation or shell-like text.

Risk: Travel searches are sent to the flyai/Fliggy service and results include provider booking links.

Mitigation: Disclose the external provider flow to users and ask them to verify prices, terms, and booking destinations before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/skills/explore-nepal)
- [Parameter Collection and Output Templates](artifact/references/templates.md)
- [Scenario Playbooks](artifact/references/playbooks.md)
- [Failure Recovery](artifact/references/fallbacks.md)
- [Execution Runbook](artifact/references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown flight-search summaries with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data and should not emit raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
