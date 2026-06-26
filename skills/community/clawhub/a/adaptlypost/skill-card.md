## Description: <br>
AdaptlyPost lets agents draft, schedule, upload media for, publish, and monitor social media posts across Instagram, X, Bluesky, TikTok, Threads, LinkedIn, Facebook, Pinterest, and YouTube through the AdaptlyPost API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tarasshyn](https://clawhub.ai/user/tarasshyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to let an agent prepare drafts, schedule posts, upload named media, cross-post to connected accounts, and check post status in AdaptlyPost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The AdaptlyPost API token can access connected social accounts in the account group. <br>
Mitigation: Use a dedicated revocable API token, connect only the accounts the agent needs, and store the token in ADAPTLYPOST_API_KEY. <br>
Risk: Posts can become public, attributable, and difficult to fully retract after publishing. <br>
Mitigation: Before every post, show the user the content, platforms, timing, and visibility settings and wait for explicit confirmation; prefer drafts for sensitive or uncertain content. <br>
Risk: Uploaded media receives a public URL as soon as the upload completes. <br>
Mitigation: Upload only files the user explicitly named, confirm exact paths first, and avoid broad directories such as Downloads, Desktop, or screenshot folders without per-file approval. <br>
Risk: Bulk or unattended posting can amplify mistakes across many queued posts. <br>
Mitigation: Confirm a small first batch before larger scheduling runs, and default unattended workflows to drafts unless the exact recurring workflow was pre-authorized. <br>
Risk: Retrying failed posts or skipped platforms silently can publish duplicate or unintended content. <br>
Mitigation: Surface errors and skipped platforms to the user and ask before retrying. <br>


## Reference(s): <br>
- [AdaptlyPost homepage](https://adaptlypost.com) <br>
- [AdaptlyPost API reference](references/api-reference.md) <br>
- [Platform-specific configs reference](references/platform-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ADAPTLYPOST_API_KEY; write actions require user confirmation and named connected accounts.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
