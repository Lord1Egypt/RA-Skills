## Description:

Query Bitpanda account data through the Bitpanda API using a bundled read-only Bash CLI for balances, trades, transactions, asset information, and live prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrtlopes](https://clawhub.ai/user/mrtlopes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect a Bitpanda account portfolio, balances, trade history, transactions, asset details, and live prices without placing orders or performing write operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled trades command can execute local commands if untrusted or agent-derived option values reach vulnerable arguments.

Mitigation: Review before installing, validate --limit and other trades parameters before execution, and avoid passing untrusted values into the CLI.

Risk: The skill requires a Bitpanda API key and can return private financial account data in command output.

Mitigation: Use a least-privilege read-only Bitpanda API key where available, run with only the required secret exposed, and avoid sharing command output in logs or transcripts.

Risk: The skill calls external Bitpanda API endpoints and depends on curl and jq being available in the runtime.

Mitigation: Run in a sandboxed environment with controlled network access to the Bitpanda API and verify curl, jq, and BITPANDA_API_KEY before use.

## Reference(s):

- [Bitpanda API Reference](references/api_reference.md)
- [Bitpanda Developer API](https://developer.bitpanda.com)
- [ClawHub Metadata Homepage](https://github.com/bitpanda-labs/agent-skills)
- [ClawHub Skill Page](https://clawhub.ai/mrtlopes/skills/bitpanda-official)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [JSON responses from the bundled Bash CLI, with Markdown guidance for command selection and interpretation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and BITPANDA_API_KEY; API output may contain private financial account data.]

## Skill Version(s):

0.1.1 (source: evidence.release.version; artifact/_meta.json lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
