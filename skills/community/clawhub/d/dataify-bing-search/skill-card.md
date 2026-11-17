## Description:

Run a general Bing web search through Dataify and return structured results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language Bing web-search requests into Dataify Scraper API calls and receive compact source links, structured results, or requested raw JSON/HTML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Endpoint override can send the Dataify API token and search details to an arbitrary URL.

Mitigation: Use only the default or a trusted allowlisted endpoint, and do not allow prompts or users to pass --url.

Risk: Search terms and precise location fields may disclose sensitive intent or location.

Mitigation: Avoid sensitive search terms and precise latitude or longitude fields unless they are necessary for the task.

Risk: Credential exposure could affect the associated Dataify account.

Mitigation: Use a dedicated Dataify token with limited value and never print, log, or paste the token into chat.

## Reference(s):

- [Dataify Bing Search API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-bing-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary by default; raw JSON or HTML when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN for live API calls and sends search parameters to the Dataify Scraper API.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
