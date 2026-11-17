## Description:

Call EngageLab App Push REST APIs to send push notifications and in-app messages to Android, iOS, and HarmonyOS devices; manage tags and aliases; create scheduled tasks and push plans; batch push; recall messages; query statistics; and configure callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devengagelab](https://clawhub.ai/user/devengagelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate EngageLab App Push API requests, helper code, and operational guidance for mobile push notifications, in-app messages, device tag and alias management, scheduling, recall, statistics, callbacks, and related push workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AppKey, Master Secret, Group Master Secret, and callback secrets for EngageLab App Push operations.

Mitigation: Use placeholders or environment variables for secrets, avoid pasting secrets into chat or shell history, and scope credentials to the minimum required application or group.

Risk: The skill can produce requests for broad or destructive actions, including broadcast sends, schedule changes, message recalls, voice deletion, and user or device deletion.

Mitigation: Require explicit user confirmation and a prior lookup of target identifiers before executing broad sends or destructive operations.

Risk: Generated helper code could be pointed at an unintended host if the base URL is changed.

Mitigation: Restrict generated or helper code to official EngageLab HTTPS API hosts for the intended data center.

## Reference(s):

- [Callback API](references/callback-api.md)
- [App Push API Error Codes](references/error-codes.md)
- [HTTP Status Code](references/http-status-code.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl, Python, Node.js, Java, or Go examples using placeholders for credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
