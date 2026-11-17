## Description:

Book airport transfer services, including private cars, shared shuttles, and limo services, using flyai CLI results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-support agents use this skill to search airport pickup, drop-off, private-car, shuttle, and limo transfer options, then present real-time booking results from flyai with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global npm CLI installation and execution can run third-party code outside the reviewed skill files.

Mitigation: Install only after reviewing the flyai CLI package, prefer a pinned and reviewed CLI version, and run it in a restricted environment.

Risk: Travel queries and local execution logs may contain sensitive itinerary or personal information.

Mitigation: Avoid entering sensitive identity, payment, account, or precise itinerary details; disable or delete .flyai-execution-log.json logging where possible.

Risk: Provider-only booking output depends on flyai detailUrl links and may not represent all available travel options.

Mitigation: Confirm each result includes a booking link from CLI output and independently review prices, provider terms, and availability before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/airport-pickup-service)
- [Publisher profile](https://clawhub.ai/user/xiejinsong)
- [Parent flyai skill](https://github.com/alibaba-flyai/flyai-skill/tree/main/skills/flyai)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel results; raw JSON is not shown to users.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
