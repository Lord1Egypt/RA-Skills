## Description:

Plan Singapore travel with real-time flight, hotel, attraction, food, and itinerary results from the flyai CLI, including booking links where available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to collect Singapore travel options, compare real-time prices, and produce bookable Markdown recommendations for flights, hotels, attractions, and destination activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to install an unpinned global CLI package.

Mitigation: Install a reviewed, pinned CLI version in an isolated environment before enabling the skill.

Risk: Travel searches may be sent to flyai or Fliggy services and booking links are included in responses.

Mitigation: Use the skill only when users accept third-party travel-search processing and clearly review booking destinations before purchase.

Risk: The runbook describes writing raw user queries to .flyai-execution-log.json.

Mitigation: Disable local query logging, redact sensitive travel details, or remove the log file after use according to data-handling policy.

## Reference(s):

- [Parameter Collection and Output Templates](references/templates.md)
- [Singapore Scenario Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands for retries or setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be sourced from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.1 (source: server release metadata; artifact frontmatter says 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
