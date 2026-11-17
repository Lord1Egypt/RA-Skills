## Description:

Operate Blockscout explorer reads through UXC with a curated OpenAPI schema, instance-specific host selection, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Blockscout explorer data for addresses, token balances, transactions, token metadata, token holders, and blocks through read-only UXC commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a mutable main-branch schema URL can change the available API surface unexpectedly.

Mitigation: Prefer linking UXC to the bundled schema file or to a pinned commit URL before installation.

Risk: Host-specific authentication could be applied to an untrusted Blockscout instance.

Mitigation: Use auth bindings only for Blockscout instances the operator trusts, and keep usage to documented GET/read operations.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/blockscout-v2.openapi.json)
- [Blockscout API Docs](https://docs.blockscout.com/devs/apis-redirect)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/blockscout-openapi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should keep automation on JSON response envelopes and preserve read-only API usage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
