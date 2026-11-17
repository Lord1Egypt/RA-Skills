## Description:

Audit the local businesses of an area to find the ones worth prospecting — list them from Google Maps with free listing verdicts (reputation, missing website, unclaimed listing, no online booking) and optional AI qualification (digital maturity, independent vs chain, size, price tier, fit with your ideal customer), pull their Google reviews, analyze the reviews per business (sentiment, praised and criticized themes, serious complaints, complaints left without a reply, 90-day trend), add emails and social profiles from each business's website, and deliver one scored CSV row per business.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxouf](https://clawhub.ai/user/maxouf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to find and assess local businesses for prospecting or reputation work. It combines public Maps listings, selected review analysis, and published business contacts into a scored CSV while guiding the user through scope and cost choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence because Skillspector's analysis was partial and some local references were unresolved.

Mitigation: Review the unresolved references and assess the complete release before relying on it.

Risk: Actor runs can incur usage charges, and an uncapped reviews request can collect every review for a place.

Mitigation: Set place and review limits, estimate cost before execution, and use the platform's run cost cap where available.

Risk: Published contact details and reviewer data may be personal data subject to local rules for collection and marketing.

Mitigation: Collect only information needed for a legitimate purpose, follow applicable direct-marketing rules, and enable reviewer links only when needed and lawfully justified.

## Reference(s):

- [Actor index](references/actor-index.md)
- [Cost guardrails and recovery](references/gotchas.md)
- [Sherwood Google Maps Scraper](https://apify.com/sherwood/google-maps-scraper)
- [Compass Google Maps Scraper](https://apify.com/compass/crawler-google-places)
- [Compass Google Maps Reviews Scraper](https://apify.com/compass/Google-Maps-Reviews-Scraper)
- [Sherwood Review Analyzer](https://apify.com/sherwood/review-analyzer)
- [Apify MCP server](https://mcp.apify.com)

## Skill Output:

**Output Type(s):** [CSV, Analysis, Guidance]

**Output Format:** [CSV with one scored row per business, plus a concise run and cost summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rows can include listing verdicts, review analysis, optional AI qualification, and published business contacts.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
