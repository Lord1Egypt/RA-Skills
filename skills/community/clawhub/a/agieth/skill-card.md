## Description:

Purchase domains, manage DNS and Cloudflare settings via agieth.ai Agent Bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larkins](https://clawhub.ai/user/larkins)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to check domain availability, create registration quotes, manage DNS records, configure Cloudflare zones and tunnels, and inspect account balances through agieth.ai. It can also support Ethereum payment workflows for domain registration when the operator supplies payment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated cryptocurrency transfers can move funds irreversibly.

Mitigation: Prefer manual wallet payment, do not expose a funded wallet private key to the agent environment, and require human approval before any blockchain transfer.

Risk: Domain registration, DNS deletion, Cloudflare changes, and hosting cancellation mutate external accounts.

Mitigation: Use a least-privilege agieth API key and require human review before executing registration, deletion, hosting, or DNS-changing actions.

Risk: The code contains ERC20 transfer functionality that is not clearly disclosed in the user-facing guide.

Mitigation: Review token-transfer behavior before installation and withhold private keys unless token transfers are explicitly intended.

Risk: Public Ethereum RPC endpoints can fail or return transaction hashes that are not later found.

Mitigation: Keep RPC failover enabled, prefer authenticated paid RPC providers for production-critical writes, and log transaction hash, RPC endpoint, and failover status.

## Reference(s):

- [Agieth homepage](https://agieth.ai)
- [Agieth API manifest](https://api.agieth.ai/api/v1/manifest)
- [ClawHub skill page](https://clawhub.ai/larkins/skills/agieth)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Python code snippets, shell commands, and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGIETH_API_KEY and AGIETH_EMAIL; automated payments require a private key and Ethereum RPC access.]

## Skill Version(s):

1.0.11 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
