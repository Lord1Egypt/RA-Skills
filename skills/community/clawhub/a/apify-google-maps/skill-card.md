## Description:

Helps an agent use an Apify actor to search Google Maps and retrieve business listings with fields such as name, address, phone, website, email, ratings, and opening hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to collect Google Maps business listing data through Apify for local business research, lead generation, deduplication, or mapping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples place the Apify token in request URLs, which can expose credentials through logs, shell history, or copied commands.

Mitigation: Use a narrowly scoped Apify token where possible, prefer authorization headers over token-in-URL examples, and avoid sharing commands or logs that contain credentials.

Risk: Email scraping may automatically visit business websites and collect contact information.

Mitigation: Treat email scraping as an explicit opt-in setting and confirm the user's target, authorization, and compliance requirements before enabling it.

Risk: The broad trigger phrases can route general local-business requests into a scraping workflow.

Mitigation: Confirm that the user intends to run Google Maps scraping through Apify before starting a run or sending queries to the third-party actor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/futurizerush/skills/apify-google-maps)
- [Apify Actor Page](https://apify.com/futurizerush/google-maps-scraper?fpr=rush)
- [Apify API Documentation](https://docs.apify.com/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, bash, JSON request, and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides Apify actor runs that return Google Maps business listing datasets; it does not create local files itself.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
