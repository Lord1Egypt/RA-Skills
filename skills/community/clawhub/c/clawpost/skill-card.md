## Description: <br>
Guides agents to post social content through the Claw Post API across X, LinkedIn, Facebook, and TikTok, including Facebook group search, join, membership checks, and group posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daydreamnationtechlabs](https://clawhub.ai/user/daydreamnationtechlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure agents to publish approved social posts, upload media, poll job status, and manage Facebook group discovery, join, and posting workflows through Claw Post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause real public posts, media uploads, and Facebook group joins through the user's logged-in browser session. <br>
Mitigation: Require explicit user approval for each post, target platform, media upload, and Facebook group join before making the corresponding API request. <br>
Risk: The paired browser extension acts through social accounts already logged in to the browser. <br>
Mitigation: Review extension permissions and Claw Post terms before installation, and use the extension only with accounts intended for agent-assisted posting. <br>
Risk: The CLAWPOST_API_KEY grants access to Claw Post actions for the account. <br>
Mitigation: Store the key only in an environment variable or secret store, never commit it to skill files, and rotate it when access is no longer needed. <br>
Risk: Uploaded media may carry sensitive content or metadata. <br>
Mitigation: Avoid sensitive media unless the user accepts the metadata and retention implications for the upload and posting workflow. <br>


## Reference(s): <br>
- [Claw Post API Docs](https://clawpost.net/api-docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/daydreamnationtechlabs/clawpost) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, code] <br>
**Output Format:** [Markdown with HTTP request snippets and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the CLAWPOST_API_KEY environment variable and a paired browser extension for external posting actions.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
