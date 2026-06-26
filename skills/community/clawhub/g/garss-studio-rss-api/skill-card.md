## Description: <br>
Use when an AI agent needs to read, refresh, summarize, or inspect RSS news from this GARSS Studio project through its backend API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoolee](https://clawhub.ai/user/zhaoolee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to help an agent authenticate to a GARSS Studio backend, read subscribed RSS items, summarize news, inspect subscriptions, and selectively refresh RSS feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may handle a GARSS Studio access code and Bearer token while calling protected endpoints. <br>
Mitigation: Use a trusted base URL, keep the access code and token private, and do not include Bearer tokens in final answers or logs. <br>
Risk: The skill can guide Docker startup and authenticated create, update, delete, or settings actions against a local GARSS Studio instance. <br>
Mitigation: Require explicit user approval before Docker startup or any mutation/settings action; prefer cached read endpoints for routine news access. <br>
Risk: Forced refresh requests fetch upstream RSS sources and update cached reader data. <br>
Mitigation: Use refresh=true only when the user explicitly asks to refresh feeds. <br>


## Reference(s): <br>
- [GARSS Studio Backend API Reference](references/api.md) <br>
- [GARSS project repository](https://github.com/zhaoolee/garss) <br>
- [ClawHub skill page](https://clawhub.ai/zhaoolee/garss-studio-rss-api) <br>
- [Publisher profile](https://clawhub.ai/user/zhaoolee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API endpoint guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated curl examples, RSS summaries, subscription details, and refresh guidance; should not expose Bearer tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
