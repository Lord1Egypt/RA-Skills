## Description: <br>
AI content platform CLI for creating workspaces, managing SEO keywords, generating article suggestions, writing articles, and publishing to WordPress, Webflow, Wix, GoHighLevel, or webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincenzor](https://clawhub.ai/user/vincenzor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and content teams use this skill to let an agent operate the Balzac CLI for workspace setup, SEO keyword management, article generation, export, and publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses BALZAC_API_KEY and can let an agent act through a Balzac account. <br>
Mitigation: Store BALZAC_API_KEY in a secure environment variable or secret manager, and avoid placing keys directly in shell commands. <br>
Risk: Balzac actions can spend credits for suggestion generation, article writing, rewrites, and image regeneration. <br>
Mitigation: Require explicit confirmation before commands that spend credits, including suggestion acceptance, direct article writing, rewrites, and cover image regeneration. <br>
Risk: Workspace deletion, settings changes, article rewrites, and publishing integrations can affect live content or account state. <br>
Mitigation: Require human review before deleting resources, changing settings, rewriting articles, or publishing to WordPress, Webflow, Wix, GoHighLevel, or webhooks. <br>


## Reference(s): <br>
- [Balzac Developer Documentation](https://developer.hirebalzac.ai) <br>
- [Balzac API Keys](https://app.hirebalzac.ai/api_keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/vincenzor/balzac) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented CLI guidance through balzac --json.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
