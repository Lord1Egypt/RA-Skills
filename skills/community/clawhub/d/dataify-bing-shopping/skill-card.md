## Description:

Search Bing Shopping for products and shopping results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn product-shopping requests into Bing Shopping searches through Dataify and receive concise product result summaries with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping queries are sent to Dataify for processing.

Mitigation: Use the skill only when sharing the query with Dataify is acceptable, and avoid submitting sensitive product-search details.

Risk: The Dataify API token can be exposed through shell history, project files, chat, or persistent environment configuration.

Mitigation: Prefer a session-scoped DATAIFY_API_TOKEN or a secret manager, never paste the token into chat or project files, and rotate it if exposure is suspected.

## Reference(s):

- [Dataify Bing Shopping API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-bing-shopping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional JSON or HTML when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product titles, links, shopping-specific fields, result counts, truncation notes, and token setup guidance when authentication is missing or invalid.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
