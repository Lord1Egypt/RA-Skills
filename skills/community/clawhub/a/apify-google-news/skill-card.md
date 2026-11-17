## Description:

Searches Google News through an Apify actor to collect news article metadata, summaries, article URLs, and available article content with region, language, date, and result-count controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to configure and run Google News searches through Apify for monitoring topics, gathering recent headlines, and retrieving structured article data for downstream review or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and request details are sent to Apify and the named third-party actor.

Mitigation: Use only non-sensitive search terms unless the user accepts that Apify and the actor publisher may process them.

Risk: The examples place the Apify token in request URLs, which can expose credentials through logs, history, or monitoring systems.

Mitigation: Use a narrowly scoped, revocable Apify token and prefer Authorization headers instead of token query parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurizerush/skills/apify-google-news)
- [Apify actor page](https://apify.com/futurizerush/google-news-scraper?fpr=rush)
- [Apify API v2 documentation](https://docs.apify.com/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python and bash examples plus JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described Apify dataset items use camelCase fields and may include article content truncated to about 2000 characters.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
