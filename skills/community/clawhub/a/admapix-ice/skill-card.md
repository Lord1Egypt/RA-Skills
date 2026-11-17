## Description:

Ad intelligence and app analytics assistant for searching ad creatives, analyzing apps, viewing rankings, tracking download and revenue estimates, and generating market insights through AdMapix APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkmcice](https://clawhub.ai/user/bkmcice)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, analysts, and developers use this skill to query AdMapix for advertising creatives, app intelligence, rankings, download and revenue estimates, ad distribution, and market analysis in English or Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deep research requests may send the user's AdMapix API key and query context to a second service.

Mitigation: Use a limited and rotatable API key, and avoid deep research flows unless the publisher removes raw key forwarding or the user explicitly accepts that data path.

Risk: Some provided shell command patterns include unsafe quoting and unbounded polling.

Mitigation: Review command construction before execution, serialize request bodies safely, and add timeouts or user cancellation for polling workflows.

Risk: Download and revenue data are third-party estimates rather than official figures.

Mitigation: Keep estimate disclaimers in user-facing responses and avoid presenting those metrics as authoritative financial or platform data.

## Reference(s):

- [AdMapix website](https://www.admapix.com)
- [Creative Search API](artifact/references/api-creative.md)
- [Product and Company API](artifact/references/api-product.md)
- [Ranking API](artifact/references/api-ranking.md)
- [Download and Revenue API](artifact/references/api-download-revenue.md)
- [App Distribution API](artifact/references/api-distribution.md)
- [Market Analysis API](artifact/references/api-market.md)
- [Parameter Mapping Reference](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, summaries, links, disclaimers, and inline shell commands when API calls are required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should match the user's language and clearly identify download and revenue figures as third-party estimates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
