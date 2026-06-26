## Description: <br>
Facebook Manager helps an OpenClaw agent manage Facebook Pages and selected account-backed workflows through Meta Graph API guidance, including page posts, comments, Messenger replies, insights, group reading, page search, and token setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trustydev212](https://clawhub.ai/user/trustydev212) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and social-media operators use this skill to configure an OpenClaw agent for Facebook Page administration, Messenger interactions, Graph API checks, and limited Facebook group or public-content discovery. The skill is most relevant when the operator already controls the relevant Meta app, page, and access tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use powerful Facebook Page or User Tokens for posting, messaging, deleting, replying, and reading social data. <br>
Mitigation: Use a dedicated least-privileged Meta app and token, avoid personal User Tokens unless they are required, and require explicit user confirmation before any write, delete, messaging, reply, or private/social-data read action. <br>
Risk: Access tokens and refresh workflows could expose account or page authority if shared, logged, or automated without review. <br>
Mitigation: Keep tokens out of logs and shared prompts, review any refresh script or cron job before use, and rotate or revoke tokens if exposure is suspected. <br>
Risk: The release evidence reports a suspicious security verdict due to broad authority and limited scoping guidance. <br>
Mitigation: Install only when the operator intentionally grants Facebook page or account authority to the agent and has reviewed the requested permissions against the intended workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trustydev212/facebook-manager) <br>
- [OpenClaw Viet Nam community](https://zalo.me/g/lajsqc334jqc5fezevvo) <br>
- [Setup guide](references/setup-guide.md) <br>
- [API reference](references/api-reference.md) <br>
- [Meta Graph API documentation](https://developers.facebook.com/docs/graph-api/) <br>
- [Meta permissions documentation](https://developers.facebook.com/docs/permissions/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and inline bash or curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Facebook Graph API requests and token-handling instructions that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
