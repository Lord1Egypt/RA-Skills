## Description:

Finds SaaS companies and software startup leads from Twitter/X using apidojo's Twitter scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, partnerships, investor outreach, and startup press users use this skill to discover and score SaaS company leads on Twitter/X by vertical, activity, profile, and launch signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twitter/X search terms, handles, profile data, and generated lead files may contain sensitive business prospect information.

Mitigation: Treat Apify requests and exported lead files as business-sensitive data and store them only in approved locations.

Risk: Token-in-URL REST examples can expose APIFY_TOKEN through shell history, logs, or copied URLs.

Mitigation: Prefer the Apify MCP flow or header-based API calls, and protect and scope APIFY_TOKEN.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-saas-company-leads-twitter)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown lead report with tables, plus inline shell, REST API, and MCP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lead data can be saved as CSV or JSON when the optional runner output flags are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
