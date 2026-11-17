## Description:

Add or update PI events in the Cloudflare D1 mb-events database using parsed event details, ISO 8601 dates, and SQL commands executed remotely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ababen](https://clawhub.ai/user/ababen)

### License/Terms of Use:

MIT-0

## Use Case:

Site maintainers for babenchuk.com use this skill to parse event details or CSV lists, generate Cloudflare D1 SQL, and verify live event updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mutate a live Cloudflare D1 events database using broad Cloudflare credentials.

Mitigation: Install only if you control the target Cloudflare account; use a dedicated least-privilege D1 token and require explicit confirmation before insert, update, or delete commands.

Risk: The skill sources credentials from a shared environment file.

Mitigation: Avoid sourcing a shared env file; provide only the scoped credentials required for the session.

Risk: Unpinned Wrangler execution can change behavior across releases.

Mitigation: Pin the Wrangler version before running generated database commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ababen/skills/add-pi-events-d1)
- [Babenchuk events page](https://babenchuk.com/#events)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL and bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands for live Cloudflare D1 database mutations; execution should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
