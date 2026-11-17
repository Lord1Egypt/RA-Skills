## Description:

Daojia helps agents summarize publicly visible JD Daojia merchant and product information, including prices, stock, reviews, and delivery timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill for lightweight analysis of public JD Daojia merchant listings, product details, category comparisons, and alert summaries. It is bounded to public-page review and excludes ordering, reverse engineering, bulk scraping, and attempts to bypass platform controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misused for account actions, ordering, scraping at scale, or attempts to bypass platform controls.

Mitigation: Use it only for lightweight summaries of publicly visible JD Daojia merchant or product pages, and do not use it for account actions, orders, bulk scraping, reverse engineering, or platform-control bypass.

Risk: Price, stock, and delivery information can vary by time and region.

Mitigation: Include the collection time and region in summaries and treat results as time-sensitive.

## Reference(s):

- [JD Daojia](https://www.jddj.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/daojia)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and comparison notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should note collection time and region when summarizing time- or location-sensitive price, stock, and delivery information.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
