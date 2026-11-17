## Description:

Finds Instagram UGC creators for brand campaigns using apidojo's Instagram scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, and influencer marketing teams use this skill to discover and score Instagram nano and micro creators for UGC campaigns, paid partnerships, and product seeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an Apify API token, which can be exposed through shared logs, repositories, or command history if handled carelessly.

Mitigation: Store APIFY_TOKEN in an environment variable or secret store, keep it out of committed files and shared logs, and prefer the MCP or helper-script path.

Risk: The REST fallback example passes the token in a query string, which can be captured by logs or monitoring systems.

Mitigation: Avoid the REST fallback unless it is changed to use safer authorization-header handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-instagram-ugc-creators-for-brands)
- [Apify actor: apidojo/instagram-scraper](https://apify.com/apidojo/instagram-scraper)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and inline shell or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CSV or JSON file output when the Apify helper script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
