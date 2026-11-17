## Description:

API Gateway helps agents call third-party APIs through Maton's managed OAuth connections for services such as Slack, HubSpot, Salesforce, Google Workspace, and Stripe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icemastert](https://clawhub.ai/user/icemastert)

### License/Terms of Use:

MIT

## Use Case:

Developers and technical operators use this skill to make HTTP requests to supported third-party services through Maton's OAuth-managed gateway and to manage authorized service connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make direct API calls that read or modify data in every OAuth connection the user authorizes.

Mitigation: Authorize only the services and scopes needed for the task, and review proposed requests before execution.

Risk: MATON_API_KEY and OAuth connection URLs are sensitive and may be exposed by examples or logs.

Mitigation: Keep credentials out of prompts, logs, and shared outputs; redact connection URLs and rotate keys if exposure is suspected.

Risk: Delete, admin, webhook, payment, file-sharing, and public-message operations can have destructive or externally visible effects.

Mitigation: Require explicit manual confirmation before high-impact operations and prefer read-only checks before write actions.

Risk: When multiple connections exist for a service, using the default connection can target the wrong account.

Mitigation: Specify the intended Maton-Connection ID for sensitive or account-specific actions.

## Reference(s):

- [Maton homepage](https://maton.ai)
- [Maton API reference](https://www.maton.ai/docs/api-reference)
- [Provider routing references](references/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with HTTP examples, Python snippets, shell commands, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and explicitly authorized OAuth connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
