## Description: <br>
OpenClaw skill that provides a WordPress REST API CLI for posts, pages, categories, tags, users, and custom requests using plain HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akkualle](https://clawhub.ai/user/akkualle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate WordPress REST API workflows for content, taxonomy, user lookups, and custom requests through a Node.js CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, or publish WordPress content when supplied credentials permit those actions. <br>
Mitigation: Use a dedicated low-privilege WordPress application password, prefer draft status for content changes, and require human review before publishing or deleting. <br>
Risk: The users commands and raw request command may expose sensitive site data or perform broad API operations. <br>
Mitigation: Limit the WordPress account role to the minimum required permissions and require human approval before reading user data or running custom requests. <br>
Risk: Credential handling mistakes could leak WordPress application passwords, basic tokens, or JWTs. <br>
Mitigation: Provide credentials through environment variables, avoid logging tokens, and do not commit credential files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/akkualle/akkualle-wordpress-api) <br>
- [Publisher profile](https://clawhub.ai/user/akkualle) <br>
- [WordPress REST API Guide](assets/wordpress-rest-api-guide.md) <br>
- [Environment variable example](env_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables for WordPress base URL and credentials; CLI exits non-zero on errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
