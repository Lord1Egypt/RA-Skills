## Description:

Extracts TikTok comments from public videos or creators with Apidojo's TikTok Comments scraper on Apify and helps analyze them for sentiment, feedback, top comments, and audience research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, market researchers, brand managers, content creators, and analysts use this skill to collect public TikTok comment data and turn it into sentiment summaries, audience signals, common questions, top comments, and product feedback insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends TikTok URLs and resulting public comments or usernames to Apify or Apidojo for processing.

Mitigation: Use the skill only when that processing is intended, and minimize or anonymize exported commenter identifiers where possible.

Risk: The artifact documents a token-in-query REST fallback, which can expose credentials in logs, browser history, or shared command transcripts.

Mitigation: Prefer an Authorization header or official Apify tooling, and use a least-privilege Apify token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/extracting-tiktok-comments-for-research)
- [ClawHub publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify actor: apidojo/tiktok-comments-scraper](https://apify.com/apidojo/tiktok-comments-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples, structured analysis tables, and optional CSV or JSON dataset outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public commenter usernames, comment text, like counts, reply counts, and timestamps; requires an Apify token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
