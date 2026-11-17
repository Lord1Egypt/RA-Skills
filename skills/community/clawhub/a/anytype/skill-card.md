## Description:

Interact with Anytype through anytype-cli and its local HTTP API to read, create, update, search, and organize objects and pages in Anytype spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tadas-subonis](https://clawhub.ai/user/tadas-subonis)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to set up Anytype CLI access, authenticate with an API key, manage spaces, and automate Anytype knowledge-base workflows. It is intended for creating, searching, linking, and organizing Anytype objects while respecting known API constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill package includes private instance setup details such as space IDs, invite data, tag IDs, collection IDs, and sharing-link components.

Mitigation: Remove SETUP.md from the release or replace instance-specific values with placeholders, and rotate or revoke exposed invite/hash values if they are real.

Risk: The skill supports delete and delete-and-recreate workflows for content updates, which can cause high-impact data loss or broken references.

Mitigation: Require explicit user confirmation, fetch and preserve existing content, maintain a recoverable backup, and update dependent references before destructive operations.

Risk: The skill depends on ANYTYPE_API_KEY and local Anytype API access, so broad bot permissions or shared workspace secrets can expose private Anytype content.

Mitigation: Use a narrowly scoped bot account where possible and store the API key in a locked-down secret store or file outside shared workspace content.

## Reference(s):

- [Anytype API Reference](references/api.md)
- [Anytype Developer Documentation](https://developers.anytype.io)
- [anytype-cli](https://github.com/anyproto/anytype-cli)
- [Anytype OpenAPI 2025-11-08](https://raw.githubusercontent.com/anyproto/anytype-api/main/docs/reference/openapi-2025-11-08.yaml)
- [ClawHub Skill Page](https://clawhub.ai/tadas-subonis/skills/anytype)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, API paths, and JSON request examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ANYTYPE_API_KEY and a locally running Anytype API service at http://127.0.0.1:31012.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
