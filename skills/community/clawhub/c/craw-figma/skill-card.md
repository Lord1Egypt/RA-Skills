## Description:

Full bidirectional Figma integration for reading files through the REST API and creating, modifying, deleting, auditing, tokenizing, and exporting design content through a local connector and Figma plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[missionarteemis-cloud](https://clawhub.ai/user/missionarteemis-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design automation agents use this skill to inspect Figma files, generate or update layers, run design and accessibility analysis, extract tokens, and export assets while working with Figma Desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local connector can make powerful changes to live Figma files, including deletion and export.

Mitigation: Use the skill only on files where automated modification and export are acceptable, and require explicit review before delete, bulk-edit, import, or export commands.

Risk: The Figma access token enables REST API access to the user's Figma account.

Mitigation: Keep FIGMA_ACCESS_TOKEN out of shared logs and files, scope access appropriately, and rotate the token if exposure is suspected.

Risk: Running connector or package-install workflows from untrusted code can execute local commands.

Mitigation: Install only trusted releases, review connector code before running it, avoid unpinned npx workflows, and stop the connector when it is not in use.

## Reference(s):

- [Figma REST API Reference](references/figma-api-reference.md)
- [UI Design Patterns - Figma Best Practices](references/design-patterns.md)
- [Figma Plugin API Overview](https://www.figma.com/plugin-docs/api/api-overview/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON command payloads, and generated code or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Figma REST API requests and local connector commands when the required token, plugin, and connector are configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
