## Description:

Helps agents read, summarize, compare, extract from, and update Feishu wiki or docx pages through Feishu OpenAPI workflows, with Markdown output preferred for analysis and JSON output available for API debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carryours](https://clawhub.ai/user/carryours)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to work with Feishu documents: reading wiki/docx links, producing concise summaries or structured extracts, comparing document content, and inserting local images back into target documents when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Feishu credentials and access tokens may be stored locally in plaintext.

Mitigation: Prefer environment variables or a dedicated low-scope Feishu app, avoid committing local token/config files, and restrict permissions on .feishu-user-token.json and .feishu-oauth-config.json.

Risk: Write-capable workflows can modify the wrong Feishu document or insert unintended local images.

Mitigation: Confirm document targets and local image paths before executing write or image insertion workflows, and use the least-privileged Feishu permissions available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carryours/skills/feishu-doc-skill)
- [Publisher profile](https://clawhub.ai/user/carryours)
- [Feishu OpenAPI](https://open.feishu.cn/open-apis)
- [Feishu OAuth authorization endpoint](https://open.feishu.cn/open-apis/authen/v1/index)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries or JSON command output, with shell commands and configuration guidance for OAuth, reading documents, and inserting local images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include document title, source link, concise summary, requested key information, target document, write result, and explicit failure reason.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
