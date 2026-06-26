## Description: <br>
Intelligently categorize, prioritize, and draft replies for emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to summarize inbox contents, classify email priority, and draft replies for review. It supports signed-in webmail access through available agent tools or direct pasted email content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read emails from a signed-in mailbox when the user asks it to triage email. <br>
Mitigation: Give narrow instructions such as account, folder, search terms, unread-only status, or message count before running triage. <br>
Risk: Generated reply drafts may be incomplete, inaccurate, or mismatched to the sender context. <br>
Mitigation: Review and edit every draft before sending; the skill does not send emails automatically. <br>


## Reference(s): <br>
- [Email Triage Pro on ClawHub](https://clawhub.ai/tommot2/email-triage-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, category counts, and reply drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are presented for user review and are not sent automatically.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
