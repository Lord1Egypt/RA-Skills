## Description:

Auto-fetches Solana address or program transactions, validates Solana addresses, and optionally decodes Anchor IDL instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkkchen](https://clawhub.ai/user/lkkchen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they need an agent to scaffold or reuse a local Solana log-pulling project, validate one or more addresses, fetch transactions, parse outputs, and report the generated files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create a local project and immediately install npm dependencies.

Mitigation: Review the proposed commands first and prefer running dependency installation yourself from a locked dependency set.

Risk: The skill may persist a Helius API key in a project .env file.

Mitigation: Use a temporary or restricted Helius key, keep .env gitignored and permission-restricted, and avoid printing the key in command output or responses.

Risk: Transaction pulls send target addresses to Helius or the Solana public RPC endpoint and may consume API quota.

Mitigation: Confirm the target addresses are appropriate to query externally and use a bounded --limit pull when full historical sync is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lkkchen/skills/fetch-solana-logs)
- [English skill instructions](artifact/SKILL.md)
- [Reference](artifact/reference.md)
- [Examples](artifact/examples.md)
- [Chinese skill instructions](artifact/SKILL.zh.md)
- [Helius RPC endpoint used by the generated project](https://mainnet.helius-rpc.com/?api-key=${key})
- [Solana public RPC fallback used by the generated project](https://api.mainnet-beta.solana.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, TypeScript, JSON, and dotenv snippets; generated project runs write NDJSON transaction logs and parsed JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized under output/<addr>/ and may include tx_logs_<addr>.txt, tx_logs_parsed_<addr>.json, and idl_<addr>.json when an IDL is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
