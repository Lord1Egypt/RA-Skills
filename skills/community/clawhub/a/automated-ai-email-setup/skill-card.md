## Description: <br>
Create and manage receive-only AI email addresses for agent signup, message retrieval, long-polling, and verification-code extraction through aiemailservice.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcgsync-git](https://clawhub.ai/user/tcgsync-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and automation agents use this skill to create receive-only mailboxes, retrieve incoming messages, wait for verification emails, and extract OTP or confirmation codes during account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may use generated mailboxes for signups, OTPs, MFA, password resets, account recovery, or personal or regulated data without clear user-consent boundaries. <br>
Mitigation: Require explicit approval before using this skill for those workflows, and avoid personal or regulated data unless the user has approved that handling. <br>
Risk: The generated API key can read messages and delete mailboxes. <br>
Mitigation: Treat the API key as a credential, avoid logging it, keep it scoped to the task, and discard or rotate it when the mailbox workflow is complete. <br>
Risk: The skill depends on aiemailservice.com as third-party receive-only mail infrastructure. <br>
Mitigation: Install and use it only when the user wants aiemailservice.com mailboxes, and confirm that the destination service permits disposable or agent-managed email addresses. <br>


## Reference(s): <br>
- [AI Email Service](https://aiemailservice.com) <br>
- [ClawHub release page](https://clawhub.ai/tcgsync-git/automated-ai-email-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls] <br>
**Output Format:** [Markdown instructions with HTTP, JavaScript, and cURL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces receive-only mailbox workflow guidance; no email sending capability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
