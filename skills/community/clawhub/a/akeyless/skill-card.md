## Description:

Akeyless IO helps agents use the official Akeyless CLI to install the tool, configure profiles, route through gateways, and perform cautious read/list operations without exposing credentials or secret values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanshak](https://clawhub.ai/user/deanshak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide an agent through Akeyless CLI setup, profile-aware commands, gateway routing, inventory checks, and safe summaries of read-only results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may handle commands for a secrets-management CLI in an authenticated environment.

Mitigation: Keep Akeyless roles least-privileged, configure credentials outside chat, and start with read-only commands when validating access.

Risk: Command output or profile files may contain secret material or sensitive account details.

Mitigation: Do not paste access keys, secret values, or ~/.akeyless profile contents into chat, logs, or repositories; summarize JSON output and redact sensitive fields.

Risk: Incorrect tenant, region, or gateway routing can produce failed access or accidental operations in the wrong environment.

Mitigation: Use the organization's documented tenant or gateway URL and verify profile, role, folder path, and AKEYLESS_GATEWAY_URL before deeper operations.

## Reference(s):

- [Akeyless IO skill page](https://clawhub.ai/deanshak/skills/akeyless)
- [Akeyless CLI documentation](https://docs.akeyless.io/docs/cli)
- [Akeyless CLI reference](https://docs.akeyless.io/docs/cli-reference)
- [Akeyless authentication methods](https://docs.akeyless.io/docs/access-and-authentication-methods)
- [Akeyless SAML authentication](https://docs.akeyless.io/docs/auth-with-saml)
- [Akeyless CLI authentication reference](https://docs.akeyless.io/docs/cli-ref-auth)
- [Akeyless list-items reference](https://docs.akeyless.io/docs/cli-reference#list-items)
- [Akeyless CLI notes](references/cli-notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise JSON-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local akeyless binary, user-managed authentication, and profile or gateway configuration outside chat.]

## Skill Version(s):

1.0.0 (source: server release metadata, changelog dated 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
