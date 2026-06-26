## Description: <br>
Draft external emails for human approval before sending. Use when communicating with external parties (support, competitions, businesses). Always draft first, send to Stef for approval, then send only after explicit approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this workflow to prepare external emails for support tickets, competition entries, business inquiries, and partnership discussions while requiring Stef's explicit approval before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External emails may expose secrets, credentials, internal-only details, or unnecessary personal data if reviewed too quickly. <br>
Mitigation: Before approval, review recipients, subject, body, CCs, and copied context, then remove sensitive or unnecessary information. <br>
Risk: Sending depends on an external email_manager.py and configured email credentials that are not included in the skill. <br>
Mitigation: Verify the email manager, credentials, and delivery configuration separately before approving any send. <br>


## Reference(s): <br>
- [Email Approval Workflow on ClawHub](https://clawhub.ai/stefanferreira/email-approval-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with email draft templates and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human approval before sending; the external email manager and credentials are not bundled with the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
