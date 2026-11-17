## Description:

Use when checking Ahrefs Domain Rating, DR, website authority, domain authority, backlink profile strength, or free Ahrefs public API data for a domain or URL without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharkqwy](https://clawhub.ai/user/sharkqwy)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve Ahrefs Domain Rating for one or more domains or URLs through Ahrefs' free public endpoint. It supports quick website authority checks and backlink profile strength comparisons without requiring an Ahrefs API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied domains or URLs are sent to Ahrefs' public API.

Mitigation: Avoid checking private or sensitive URLs when disclosure to Ahrefs is not acceptable.

Risk: Installing through unpinned npx-based flows can run package-manager-resolved code.

Mitigation: Install through ClawHub when possible, or pin and review npx-based installers before use.

## Reference(s):

- [Ahrefs Domain Rating Free API Documentation](https://docs.ahrefs.com/en/api/reference/public/get-domain-rating-free)
- [Ahrefs Domain Rating Free Endpoint](https://api.ahrefs.com/v3/public/domain-rating-free)
- [ClawHub Skill Page](https://clawhub.ai/sharkqwy/skills/ahrefs-domain-rating-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with optional plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapper can return compact text, machine-readable JSON, or raw Ahrefs JSON per target.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
