## Description:

Fetch live public web data with the Datapika actors on Apify. Use when the user asks for job listings or hiring signals (LinkedIn, Indeed, Glassdoor, ZipRecruiter, company career sites), Reddit posts or comments, TikTok, Douyin, Bilibili, Kuaishou, YouTube, Threads or WeChat content, TikTok Shop products, Trustpilot reviews, Facebook/Instagram or Google ads, Google Maps places, Airbnb listings, hotel prices or Google Flights fares, and wants real rows instead of a guess.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openciawai](https://clawhub.ai/user/openciawai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use Datapika to retrieve current public listings, posts, reviews, advertisements, places, and travel information from supported sites. The skill guides selection and setup of an Apify actor and returns its collected rows for the user's request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests and the Apify token are handled by Apify when actors are run.

Mitigation: Use the service only if you trust Apify with the request data and token; do not expose the token in output or share it unnecessarily.

Risk: Actor runs may incur charges for each result.

Mitigation: Check current actor pricing and set result limits to the amount of data needed before running an actor.

Risk: Collected names, profiles, and reviews may contain personal data.

Mitigation: Collect public data only and retain only what the task needs, following applicable privacy requirements.

Risk: Security inspection was partial because two local path-like references could not be matched to bundled artifacts.

Mitigation: Review those references and their behavior before relying on them.

## Reference(s):

- [Datapika skill release](https://clawhub.ai/openciawai/skills/datapika)
- [Datapika actors and pricing](https://datapika.com/actors)
- [Datapika MCP setup](https://datapika.com/mcp)
- [Datapika examples](https://github.com/lnvestor/datapika-examples)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Rows returned by the selected Apify actor as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields and row counts vary by actor; runs may incur charges per result on the user's Apify account.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
