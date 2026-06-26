## Description: <br>
Eversince is a creative agent that plans and executes across image, video, and audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eversince-ai](https://clawhub.ai/user/eversince-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to brief Eversince, manage creative media projects, generate or assemble image, video, and audio assets, and monitor costs and results through the Eversince API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid creative generations can consume Eversince account credits. <br>
Mitigation: Check account credits and estimate costs before starting generation work. <br>
Risk: The skill requires a sensitive Eversince API key. <br>
Mitigation: Use a dedicated revocable API key and revoke or rotate it when access is no longer needed. <br>
Risk: Uploaded media, references, and URLs are sent to an external Eversince service. <br>
Mitigation: Avoid uploading confidential media unless the user's data-handling requirements allow it. <br>
Risk: Public share links, webhooks, learned preferences, account skills, and API key changes can affect account state or expose content. <br>
Mitigation: Require explicit user approval before creating public share links, setting webhooks, changing learned preferences or account skills, or creating/revoking API keys. <br>


## Reference(s): <br>
- [Eversince Documentation](https://docs.eversince.ai) <br>
- [Eversince Homepage](https://eversince.ai) <br>
- [API Reference](references/api-reference.md) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/eversince-ai/eversince) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Eversince API with a user-provided API key and return project status, creative guidance, generated asset links, rendered video links, or account cost information.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
