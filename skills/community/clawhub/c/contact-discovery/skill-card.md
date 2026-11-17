## Description:

Find public contact details for a person or company using Prismfy-powered web search before outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jernejcicorbin-hub](https://clawhub.ai/user/jernejcicorbin-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find public email addresses, contact pages, press or support paths, and company email-format clues before outreach. It is intended for source-backed public contact discovery, not private-data inference or guessed personal emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Prismfy API key with meaningful quota, billing, or access can be exposed through persistent shell-profile setup or unsafe endpoint overrides.

Mitigation: Use a secret manager or per-command environment injection, avoid storing the key in ~/.bashrc, and set endpoint override variables only for endpoints you control.

Risk: Contact lookup queries are sent to Prismfy and may include person, company, domain, role, or outreach context.

Mitigation: Submit only the public identifiers needed for the lookup and review whether the query content is appropriate for the account and workflow.

Risk: Email-format clues or weak public evidence can be mistaken for a confirmed personal email address.

Mitigation: Treat only explicitly published emails as found, label pattern-only results as clues, and require human review before high-value outreach.

## Reference(s):

- [Prismfy](https://prismfy.io)
- [ClawHub skill page](https://clawhub.ai/jernejcicorbin-hub/skills/contact-discovery)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Concise chat text with source URLs, plus an optional JSON report when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PRISMFY_API_KEY, curl, and jq; contact lookup queries are sent to Prismfy.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
