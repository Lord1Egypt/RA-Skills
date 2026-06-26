## Description: <br>
Akeyless IO helps agents use the official akeyless CLI to install and configure profiles, route through gateways, and perform safe read/list operations without exposing credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanshak](https://clawhub.ai/user/deanshak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent check Akeyless CLI setup, guide local authentication, inspect secret inventory with read-only commands, and summarize results without revealing secret values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could expose Akeyless access keys, secret values, or profile contents in chat, logs, or repositories. <br>
Mitigation: Run authentication locally outside chat, never paste credentials or profile files, and redact or omit secret-bearing fields when summarizing JSON output. <br>
Risk: The agent could operate with broader Akeyless access than intended. <br>
Mitigation: Use a least-privileged Akeyless profile limited to the folders and operations needed, and start with read-only list operations. <br>
Risk: Commands could target the wrong Akeyless gateway, tenant, or region. <br>
Mitigation: Verify the active profile, documented tenant URL, and AKEYLESS_GATEWAY_URL before running CLI operations. <br>


## Reference(s): <br>
- [Akeyless CLI documentation](https://docs.akeyless.io/docs/cli) <br>
- [Akeyless CLI reference](https://docs.akeyless.io/docs/cli-reference) <br>
- [Akeyless authentication methods](https://docs.akeyless.io/docs/access-and-authentication-methods) <br>
- [Auth with SAML](https://docs.akeyless.io/docs/auth-with-saml) <br>
- [Akeyless CLI notes](references/cli-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/deanshak/akeyless) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise JSON-output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local akeyless binary and an authenticated, least-privileged Akeyless profile on the gateway host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
