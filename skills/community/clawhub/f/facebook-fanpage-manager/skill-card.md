## Description: <br>
Helps an agent manage Facebook Fanpage workflows through the Facebook Graph API, including posting, comment replies, Messenger auto-replies, insights checks, and Page ID and Page Access Token setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trustydev212](https://clawhub.ai/user/trustydev212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, page operators, and social media teams use this skill to configure OpenClaw for Facebook Fanpage operations and to generate Graph API commands for posts, comments, Messenger responses, and page insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a Facebook Page with a long-lived access token, including posting, messaging, and comment actions. <br>
Mitigation: Review requested Facebook permissions before installation, start with a test or low-risk page, and use human review or audit controls for outgoing posts, comments, and messages. <br>
Risk: Facebook Page access tokens may be exposed through local configuration, logs, screenshots, or diagnostic output. <br>
Mitigation: Store the access token with a protected secret mechanism when possible, restrict local configuration permissions, avoid sharing connection-check output, and rotate or revoke the token if exposure is suspected. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [API Reference](references/api-reference.md) <br>
- [OpenClaw Viet Nam community](https://zalo.me/g/lajsqc334jqc5fezevvo) <br>
- [Facebook Graph API documentation](https://developers.facebook.com/docs/graph-api/) <br>
- [Messenger Platform documentation](https://developers.facebook.com/docs/messenger-platform/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus FACEBOOK_PAGE_ID and FACEBOOK_ACCESS_TOKEN environment values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
