## Description: <br>
Fetches recent emails from Gmail and provides concise summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbdyno](https://clawhub.ai/user/bbdyno) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and external users use this skill to review unread Gmail messages quickly, with sender, subject, summary, key points, and suggested actions surfaced in an easy-to-scan report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and summarizes unread Gmail messages, which can expose sensitive mailbox content to the agent workflow. <br>
Mitigation: Install only for accounts where this access is acceptable, and use a dedicated Google OAuth client with read-only Gmail access. <br>
Risk: OAuth credentials and token.json are stored locally near the configured credentials file. <br>
Mitigation: Protect the credentials path and token file with appropriate local file permissions and avoid sharing them across workspaces. <br>
Risk: The published homepage appears to be a placeholder, so source identity is less clear than a server-resolved repository import. <br>
Mitigation: Verify the ClawHub publisher and source before deployment, especially in sensitive environments. <br>
Risk: The skill depends on Python Gmail API packages at broad version ranges. <br>
Mitigation: Pin or review dependencies before use in sensitive or managed environments. <br>


## Reference(s): <br>
- [Daily Email Summary on ClawHub](https://clawhub.ai/bbdyno/email-summary) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Gmail API read-only scope](https://www.googleapis.com/auth/gmail.readonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary report based on JSON returned by the Gmail helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes sender, subject, date, summary, key points, and suggested action for each fetched unread email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
