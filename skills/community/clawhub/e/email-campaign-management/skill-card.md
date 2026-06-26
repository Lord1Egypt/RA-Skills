## Description: <br>
Complete workflow for email marketing campaigns with conversion tracking, reminder emails, campaign reports, and trial activation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urbantech](https://clawhub.ai/user/urbantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Growth, marketing, and product engineers use this skill to create email campaigns, send campaign messages through Resend, track clicks and conversions, activate user trials, and generate campaign reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campaign workflows can send real email to recipient lists. <br>
Mitigation: Require explicit human approval for each recipient list and campaign send, and test in staging or with a dry run before production delivery. <br>
Risk: Trial activation examples can change live subscription or trial status. <br>
Mitigation: Use least-privilege database credentials, review every subscription update before execution, and prepare rollback steps before applying changes. <br>
Risk: Marketing email workflows can create compliance issues if recipient consent or unsubscribe handling is not confirmed. <br>
Mitigation: Confirm opt-in status, unsubscribe requirements, and campaign compliance obligations before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urbantech/email-campaign-management) <br>
- [Publisher profile](https://clawhub.ai/user/urbantech) <br>
- [Resend email API endpoint](https://api.resend.com/emails) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, Python, HTML, CSS, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workflow checklists and operational guidance for campaign sends, analytics, and trial activation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
