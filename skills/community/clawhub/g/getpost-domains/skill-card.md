## Description:

Register domains, manage DNS, and set up email sending via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check domain availability, register domains, manage DNS records, and configure email authentication through the GetPost API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide account signup, domain purchases, DNS changes, redirects, and email-authentication setup.

Mitigation: Require explicit user confirmation before any signup, purchase, registration, nameserver, DNS, redirect, or email-authentication change.

Risk: The skill uses a bearer API key for GetPost API access.

Mitigation: Store the API key outside prompts and shared logs, and avoid exposing it in generated commands or transcripts.

## Reference(s):

- [GetPost Domains API documentation](https://getpost.dev/docs/api-reference#domains)
- [ClawHub skill page](https://clawhub.ai/dommholland/skills/getpost-domains)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include domain registration, DNS, redirect, and email-authentication steps that require user approval before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
