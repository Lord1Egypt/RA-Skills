## Description:

Rotating Apify API key manager that returns the least-recently-used active Apify key from the ColdCore database before Apify API calls that need available credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aces1up](https://clawhub.ai/user/aces1up)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to retrieve, rotate, list, and optionally balance-check Apify API keys backed by a ColdCore MySQL database before making Apify API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded database credentials and exposed API keys can disclose or compromise owned accounts.

Mitigation: Rotate exposed credentials, move secrets to environment variables or a secret manager, and install only in environments authorized for the ColdCore database and Apify accounts.

Risk: List and JSON output can reveal API keys and account metadata to logs or unauthorized callers.

Mitigation: Redact API keys in list output, restrict invocation to authorized agents or users, and avoid logging returned key material.

Risk: Runtime package installation mutates the host Python environment.

Mitigation: Preinstall dependencies in an isolated environment and remove runtime pip installation from the operational path.

Risk: The key rotation flow writes usage state back to the database.

Mitigation: Use least-privilege database credentials, verify the target database before deployment, and audit updates to key usage state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aces1up/skills/apify-keys)
- [Apify monthly usage API endpoint](https://api.apify.com/v2/users/me/usage/monthly)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text API key or JSON object, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May expose secrets if installed or invoked without access controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
