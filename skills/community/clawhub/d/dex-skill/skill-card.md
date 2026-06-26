## Description: <br>
Manage your Dex personal CRM by searching, creating, and updating contacts; logging interaction notes; setting follow-up reminders; organizing contacts with tags and groups; and managing custom fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ocruzv](https://clawhub.ai/user/ocruzv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Dex personal CRM records, prepare for meetings, log relationship history, schedule follow-ups, and organize professional contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change sensitive Dex CRM records. <br>
Mitigation: Install only when the user trusts Dex, the Dex MCP server, and the @getdex/cli package with CRM data. <br>
Risk: Bulk edits, deletions, merges, note creation, reminders, and contact updates can materially alter CRM data. <br>
Mitigation: Require explicit user confirmation before destructive or bulk-changing operations. <br>
Risk: Dex API keys grant access to personal CRM data. <br>
Mitigation: Keep API keys private, use secure local storage or environment variables, and review which AI clients receive MCP access. <br>


## Reference(s): <br>
- [Dex skill listing](https://clawhub.ai/ocruzv/dex-skill) <br>
- [Dex homepage](https://getdex.com) <br>
- [Dex MCP setup guide](https://getdex.com/docs/ai/mcp-server) <br>
- [CLI Command Reference](references/cli-commands.md) <br>
- [CRM Workflows](references/crm-workflows.md) <br>
- [Dex Tools Reference](references/tools-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Dex MCP tools or guide CLI setup; responses can include CRM summaries, proposed record changes, reminders, notes, and contact-organization guidance.] <br>

## Skill Version(s): <br>
2.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
