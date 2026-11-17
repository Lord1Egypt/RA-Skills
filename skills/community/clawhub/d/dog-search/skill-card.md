## Description:

Search Google through the ScrapingDog API using the bundled Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to run a Google search through ScrapingDog and return formatted results or raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to ScrapingDog and Google, which can expose confidential or sensitive query text.

Mitigation: Avoid searching secrets or confidential text, and only install the skill when that data flow is acceptable.

Risk: The skill requires a ScrapingDog API key.

Mitigation: Use a dedicated key with usage limits and keep it in the SCRAPINGDOG_API_KEY environment variable.

Risk: The current CLI appears to reference an unavailable results argument.

Mitigation: Avoid relying on configurable result counts until the CLI argument bug is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goog/skills/dog-search)
- [ScrapingDog Google API endpoint](https://api.scrapingdog.com/google)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text search results by default, with optional JSON output and Markdown command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCRAPINGDOG_API_KEY and Python; search requests are sent to ScrapingDog and Google.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
