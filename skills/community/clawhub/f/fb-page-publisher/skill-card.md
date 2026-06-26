## Description: <br>
Publish posts, upload photos, schedule content, read insights, and manage comments on Facebook Pages via the Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaimin-345](https://clawhub.ai/user/jaimin-345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators, marketers, and developers use this skill to let an agent publish, schedule, inspect, and moderate Facebook Page content through the Facebook Graph API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can publish, schedule, reply to, and delete live Facebook Page content using the configured Page token. <br>
Mitigation: Use a test Page first when possible and configure the MCP host to require explicit human approval before content-changing actions. <br>
Risk: A long-lived Facebook Page access token grants real Page authority if exposed or over-permissioned. <br>
Mitigation: Store FB_ACCESS_TOKEN as a secret, use least-privilege and revocable credentials, and rotate or revoke the token if access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaimin-345/fb-page-publisher) <br>
- [Facebook Developers](https://developers.facebook.com) <br>
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>
- [Facebook Graph API v21.0](https://graph.facebook.com/v21.0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Human-readable text returned by MCP tools, with setup guidance and JSON configuration examples in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls may publish, schedule, reply to, or delete live Facebook Page content when configured with valid Page credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
