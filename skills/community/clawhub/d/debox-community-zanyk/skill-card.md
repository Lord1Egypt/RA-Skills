## Description:

Manage DeBox communities, DAOs, and NFT groups. Use when you need to verify group membership, check voting/lottery participation, query group info, or validate user eligibility for DAO/NFT communities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanyk4502](https://clawhub.ai/user/zanyk4502)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and community operators use this skill to query DeBox group information, verify DAO or NFT community membership, check voting and lottery participation, and generate user profile reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a bundled config.json with a real-looking DeBox API key.

Mitigation: Remove the bundled key before installation and provide a user-controlled key through environment variables or another secret-management mechanism.

Risk: Profile and image-report commands can send user IDs or wallet addresses to DeBox and write files locally.

Mitigation: Use these commands only for intended users and paths, review identifiers before execution, and avoid running the CLI with elevated privileges.

Risk: Server security evidence marks the skill as suspicious due to secret handling and profile-image network and file behavior.

Mitigation: Review the skill and its configuration before deployment, rotate any exposed API key, and limit execution to trusted workspaces.

## Reference(s):

- [DeBox API Reference](references/api.md)
- [DeBox Developer Platform](https://developer.debox.pro)
- [DeBox Open API](https://open.debox.pro/openapi)
- [ClawHub Skill Page](https://clawhub.ai/zanyk4502/skills/debox-community-zanyk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output, JSON-like API responses, Markdown documentation, and optional generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a DeBox API key and may send wallet addresses, user IDs, group URLs, and chain IDs to DeBox APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
