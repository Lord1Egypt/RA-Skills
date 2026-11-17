## Description:

Extract comments and replies from TikTok video and photo posts using the futurizerush/tiktok-comment-scraper Apify Actor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to run an Apify scraper for public TikTok posts and retrieve comments and replies for engagement analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens placed in request URLs can be exposed through logs, shell history, proxies, or copied examples.

Mitigation: Use a narrow, revocable Apify token and prefer Authorization headers or other non-URL credential handling when adapting the examples.

Risk: TikTok URLs, scraping settings, and collected comment data are processed by Apify.

Mitigation: Confirm that sending the requested TikTok inputs and outputs to Apify is acceptable for the user's privacy, policy, and data-handling requirements before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurizerush/skills/apify-tiktok-comments)
- [Apify TikTok Comment Scraper Actor](https://apify.com/futurizerush/tiktok-comment-scraper?fpr=rush)
- [Apify API v2 documentation](https://docs.apify.com/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash examples that produce JSON results from Apify datasets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe Apify API calls, polling behavior, input parameters, and returned TikTok comment and reply fields.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
