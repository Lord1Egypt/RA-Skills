## Description:

Interacts with the Bitpanda API to retrieve raw portfolio, trade, and price data with pagination and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattialagreca](https://clawhub.ai/user/mattialagreca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Bitpanda users use this skill to retrieve raw portfolio balances, complete wallet data, trade history, and asset prices for their own downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Bitpanda API key and may expose financial account credentials if the key is pasted into command history, logs, shell profiles, chats, screenshots, or shared terminals.

Mitigation: Use a least-privilege API key where available, prefer session-scoped environment variables, avoid passing secrets as command-line arguments, and rotate or revoke any key that may have been exposed.

Risk: Command output can include private portfolio, trade, balance, and price data.

Mitigation: Treat all generated output as private financial data and avoid sharing raw command results outside trusted environments.

Risk: The release has a suspicious security verdict due to under-disclosed storage and output risks.

Mitigation: Review the skill before installation and confirm that local credential handling and output handling match the user's security requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mattialagreca/skills/bitpanda-v2)
- [Bitpanda Developer Portal](https://developers.bitpanda.com/)
- [Bitpanda API Base URL](https://developer.bitpanda.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and PowerShell examples plus JSON API output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shell command output can contain private financial account data returned by Bitpanda.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
