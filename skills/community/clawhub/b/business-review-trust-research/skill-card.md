## Description:

Researches product launches, software reviews, business reputation, startup revenue, and crowdfunding campaigns through the Crawlora API, returning normalized JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can research products and vendors before buying or partnering, and review crowdfunding campaigns before backing them. The skill gathers public launch, review, business profile, revenue, and campaign information into JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to Crawlora, and its data-retention practices were not assessed.

Mitigation: Use a dedicated Crawlora key and send only queries you are comfortable sharing with the provider.

Risk: Successful requests may consume account credits.

Mitigation: Track account usage and make requests only for the research needed.

## Reference(s):

- [Crawlora endpoint reference](artifact/reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [JSON, Business and product research]

**Output Format:** [Normalized JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be paginated; API requests may consume account credits.]

## Skill Version(s):

1.0.22 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
