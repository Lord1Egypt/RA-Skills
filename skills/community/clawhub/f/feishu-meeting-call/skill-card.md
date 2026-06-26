## Description: <br>
Sends Feishu urgent reminder messages, including in-app urgent pushes and phone-call escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to send urgent Feishu reminders to themselves or eligible users in their organization. It can look up a Feishu user by phone or email, send a reminder message, and optionally trigger phone-call escalation for urgent situations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Feishu App Secret that can send urgent reminders and phone-call escalations. <br>
Mitigation: Install only from a trusted publisher, keep .feishu.env private and out of shared workspaces or source control, and limit the Feishu app's available users and permissions. <br>
Risk: Phone-call escalation can interrupt recipients and consume enterprise quota. <br>
Mitigation: Confirm user intent before using phone-call escalation and reserve it for genuinely urgent reminders. <br>
Risk: Lookup by phone or email can expose or target other Feishu users in the same organization. <br>
Mitigation: Confirm the intended recipient before lookup or notification, and restrict the Feishu app's available scope to approved users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daxiangnaoyang/feishu-meeting-call) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu Open APIs](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and command-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Feishu credentials in FEISHU_APP_ID, FEISHU_APP_SECRET, and FEISHU_USER_OPEN_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog state 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
