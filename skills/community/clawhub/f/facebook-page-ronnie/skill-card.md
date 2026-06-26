## Description: <br>
Manage Ronnie's Facebook Page by posting text or photos, testing comment permissions, diagnosing token issues, and using browser fallback when APIs are blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ronnine6527](https://clawhub.ai/user/ronnine6527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Page operators and supporting agents use this skill to publish Facebook Page posts, verify comment or reply permissions, troubleshoot Page token and app mode issues, and choose a browser fallback when Graph API engagement actions are blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful Facebook Page access tokens and app secrets that could allow unauthorized Page actions if exposed. <br>
Mitigation: Store credentials in protected environment variables or a secret manager, avoid pasting secrets into chat or logs, and rotate any exposed tokens. <br>
Risk: The skill can publish posts, comments, replies, or browser-based actions on a Facebook Page. <br>
Mitigation: Require explicit confirmation before any post, comment, reply, or browser action that changes Page content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ronnine6527/facebook-page-ronnie) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Facebook Page ID and Page access token environment variables for API workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
