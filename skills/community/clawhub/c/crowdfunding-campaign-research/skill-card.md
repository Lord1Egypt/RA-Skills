## Description:

Compare Kickstarter campaigns through Crawlora using funding snapshots, reward tiers, creator updates, risks, and sampled backer comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and campaign teams use this skill to benchmark Kickstarter projects and prepare evidence-based funding, rewards, progress, and fulfillment briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, scraped public URLs, and the API key are sent to Crawlora.

Mitigation: Keep the key in the environment; send only public URLs and avoid sensitive personal data.

Risk: Incomplete snapshots or sampled comments can misstate funding trends, delivery outcomes, or backer sentiment.

Mitigation: Bound requests, cross-check campaign figures, identify collection dates and sample sizes, and distinguish creator claims from verified outcomes.

## Reference(s):

- [Crowdfunding Campaign Research on ClawHub](https://clawhub.ai/crawlora-org/skills/crowdfunding-campaign-research)
- [Skill endpoint reference](reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [Kickstarter project basics](https://help.kickstarter.com/hc/en-us/articles/115005028514-What-are-the-basics)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research brief with campaign links and dated comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cohort rules, reward and update comparisons, sampled comment counts, disagreements, and open questions.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
