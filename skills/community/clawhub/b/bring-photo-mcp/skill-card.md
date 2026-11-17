## Description:

Turn product photos into verified Bring! list items via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[schnueck](https://clawhub.ai/user/schnueck)

### License/Terms of Use:

MIT

## Use Case:

External Bring! users can use the skill to identify products from photos, classify them against the configured catalog, and add or manage items on allowed shopping lists with verified results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shopping-list writes can change shared Bring! lists.

Mitigation: Restrict BRING_ALLOWED_LISTS to lists the user intends to manage and verify persisted results.

Risk: An attached original photo may contain private details and may be visible to Bring! list members.

Mitigation: Request explicit authorization for original-photo uploads and remove private details first.

Risk: The separately installed npm runtime was not supplied for verification.

Mitigation: Review and pin the bring-photo-mcp package before use.

Risk: Bring! account credentials are required.

Mitigation: Store BRING_PASSWORD in a secret store and do not expose credentials in conversation output.

## Reference(s):

- [Bring Photo MCP on ClawHub](https://clawhub.ai/schnueck/skills/bring-photo-mcp)
- [Publisher profile](https://clawhub.ai/user/schnueck)

## Skill Output:

**Output Type(s):** [API calls, Text]

**Output Format:** [Bring! MCP tool calls and concise Markdown status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-list outcomes and verification evidence without exposing sensitive identifiers.]

## Skill Version(s):

1.0.3 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
