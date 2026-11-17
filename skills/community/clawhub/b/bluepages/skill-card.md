## Description:

Look up wallet address <> Twitter/Farcaster identity mappings via Bluepages.fyi for wallet ownership, social handle address discovery, 0x address lookups, and wallet identity attribution queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesse-pallok](https://clawhub.ai/user/jesse-pallok)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to resolve Ethereum wallet addresses to Twitter/X or Farcaster identities, find wallet addresses for social handles, and plan cost-conscious Bluepages API or MCP lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned remote MCP server that may receive authentication material and payment authority.

Mitigation: Prefer BLUEPAGES_API_KEY over PRIVATE_KEY, run only a pinned or audited MCP version, and use a constrained environment.

Risk: Providing PRIVATE_KEY enables x402 payments and credit purchases.

Mitigation: Use a dedicated wallet with only necessary funds and approvals, and require explicit user confirmation before financial actions.

## Reference(s):

- [Bluepages Documentation](https://bluepages.fyi/docs.html)
- [Bluepages API Keys](https://bluepages.fyi/api-keys.html)
- [ClawHub Bluepages Skill](https://clawhub.ai/jesse-pallok/skills/bluepages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text responses with optional shell and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require BLUEPAGES_API_KEY or PRIVATE_KEY authentication; x402 payments and credit purchases should remain under explicit user control.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
