## Description:

Scrapes Bluesky social posts via AT Protocol using an Apify Actor REST API and requires an APIFY_TOKEN environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to run Apify-backed Bluesky searches from an agent, fetch post data, and summarize counts, engagement, themes, or exportable results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials are placed in request URLs, which can expose them through shell tracing, logs, or command history.

Mitigation: Use a minimally scoped APIFY_TOKEN, avoid shell tracing and logging full commands, and revise the skill to use Authorization headers before deployment.

Risk: Bluesky search terms and requested limits are sent to Apify under the user's Apify account.

Mitigation: Confirm users are comfortable sharing those search parameters with Apify and avoid sending sensitive terms.

Risk: The authoritative security verdict is suspicious because the skill does not clearly warn users about third-party data sharing and credential handling.

Mitigation: Review the skill before execution and add clear user-facing warnings before broad deployment.

## Reference(s):

- [Apify Bluesky Scraper on ClawHub](https://clawhub.ai/marcindudekdev/skills/apify-bluesky-scraper)
- [Publisher profile on ClawHub](https://clawhub.ai/user/marcindudekdev)
- [Apify Actor API endpoint](https://api.apify.com/v2/acts/WAJfBnZBYR9mJrk5d)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command examples and JSON result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can summarize Bluesky post counts, engagement, common themes, and JSON or CSV export options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
