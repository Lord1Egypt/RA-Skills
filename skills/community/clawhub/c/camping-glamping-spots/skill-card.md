## Description:

Find camping grounds and glamping sites, from wild tent pitches to luxury safari tents, using flyai/Fliggy real-time travel search results with booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search for camping and glamping options by city and return comparison-style Markdown results with booking links from flyai output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a global flyai CLI dependency that may be installed without a pinned version.

Mitigation: Review and pin the @fly-ai/flyai-cli dependency before installation, and avoid automatic global npm installation in production workflows.

Risk: The artifact runbook can persist raw user queries and shell command details in a local execution log.

Mitigation: Disable logging or redact user inputs and command details before any execution data is written.

Risk: Travel answers depend on external flyai/Fliggy CLI availability and valid booking URLs.

Mitigation: Fail closed when flyai is unavailable or when results do not include detailUrl booking links, instead of filling gaps from model knowledge.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dingtom336-gif/skills/camping-glamping-spots)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown travel results with comparison tables, booking links, and occasional inline shell commands for setup or recovery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel facts, includes Book links from detailUrl values, and avoids raw JSON in user-facing responses.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
