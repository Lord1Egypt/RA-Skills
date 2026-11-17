## Description:

Check a Bitpanda crypto portfolio, wallet balances, trade history, and asset prices through a read-only CLI workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbeer](https://clawhub.ai/user/florianbeer)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query their own Bitpanda account from an agent-accessible CLI for portfolio summaries, non-zero wallet balances, trade history, and asset price or balance lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bitpanda API key can be exposed to local process inspection when passed to curl as a header argument.

Mitigation: Use a dedicated read-only Bitpanda API key with minimum scopes, avoid broader permissions, and review or revise the curl header handling before use with a sensitive key.

Risk: Transaction options for wallet and date filtering are parsed but not applied by the script.

Mitigation: Do not rely on --wallet, --from, or --to filters for transaction scoping unless those filters are implemented and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/florianbeer/skills/bitpanda)
- [Bitpanda API key settings](https://web.bitpanda.com/my-account/apikey)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal output from CLI commands, with setup guidance for environment variables or a local credentials file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, bc, and a Bitpanda API key for authenticated portfolio, wallet, and trade requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
