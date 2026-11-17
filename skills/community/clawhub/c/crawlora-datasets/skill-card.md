## Description:

Queries Crawlora's pre-built datasets to search, filter, aggregate, and retrieve public records as clean JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to search and summarize Crawlora's periodically refreshed datasets for population-level research, such as market, hiring, or app-store analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using this skill sends requests and a Crawlora API key to Crawlora's external API; scan analysis was partial because a local path-like reference could not be resolved.

Mitigation: Use a key intended for Crawlora, provide it through CRAWLORA_API_KEY, and review the unresolved reference before use.

## Reference(s):

- [Crawlora hosted dataset endpoint reference](reference/endpoints.md)
- [Crawlora datasets skill release](https://clawhub.ai/crawlora-org/skills/crawlora-datasets)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON records and aggregate results, with summaries in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be paginated and reflect scheduled dataset refreshes rather than real-time data.]

## Skill Version(s):

1.0.28 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
