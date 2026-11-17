## Description:

Authenticate an Agnic wallet through browser OAuth or headless API-token authentication for CLI, CI, server, and agent environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to check Agnic CLI authentication status, connect a wallet, configure headless token authentication, log in through browser OAuth, and resolve authentication errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm CLI during wallet credential and OAuth flows.

Mitigation: Use only after reviewing and trusting the current Agnic npm package and publisher; prefer a pinned or preinstalled reviewed CLI.

Risk: Passing an API token with the --token flag can expose the token through shell history or process listings.

Mitigation: Prefer AGNIC_TOKEN through a secure environment or secret manager, avoid inline command-line tokens, and keep wallet/API token permissions and spending limits narrow.

## Reference(s):

- [Agnic App](https://app.agnic.ai)
- [ClawHub Skill Page](https://clawhub.ai/agnicpay-prog/skills/agnicpay-authenticate-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authentication status checks, login and logout commands, token setup guidance, and expected JSON status output.]

## Skill Version(s):

2.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
