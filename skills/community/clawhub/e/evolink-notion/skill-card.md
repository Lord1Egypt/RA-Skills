## Description: <br>
Enables agents to access, create, update, and automate Notion pages and databases using the Notion API with Evolink integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read, append, create, query, and update Notion pages and databases after a Notion integration token and required page or database shares are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broadly shared Notion integration token can expose more workspace content than intended. <br>
Mitigation: Use a dedicated Notion integration token and share only the specific pages or databases needed. <br>
Risk: Schema changes, updates, or destructive actions can alter Notion data in ways that are difficult to reverse. <br>
Mitigation: Inspect schema diffs and require explicit confirmation before schema changes or destructive operations. <br>
Risk: Notion content and Evolink processing may involve sensitive information. <br>
Mitigation: Avoid highly sensitive Notion content until Evolink handling and retention expectations are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/evolinkai/evolink-notion) <br>
- [Notion Integration Setup](https://www.notion.so/my-integrations) <br>
- [Evolink API Reference](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=github&utm_medium=skill&utm_campaign=notion-skill-for-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and may use EVOLINK_API_KEY, EVOLINK_MODEL, and NOTION_PROFILE; Notion access is limited to pages and databases shared with the configured integration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
