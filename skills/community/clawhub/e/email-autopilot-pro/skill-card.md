## Description: <br>
Email Autopilot helps an agent triage email by urgency, draft replies in the user's voice, track follow-ups, manage unsubscribe queues, search email history, and produce briefings while requiring approval before sending or unsubscribing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Professionals, founders, sales, customer success, support, consultants, and freelancers use this skill to reduce inbox triage work, surface important messages, prepare reply drafts for approval, monitor follow-ups, and summarize email activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to repeatedly read and act across a sensitive mailbox, including historical and sent email. <br>
Mitigation: Confirm the account, folders, and history scope before use, and limit mailbox access to the minimum needed for the intended workflow. <br>
Risk: Automated briefings, follow-up tracking, unsubscribe handling, and style learning may create unwanted actions or retain sensitive communication patterns. <br>
Mitigation: Enable recurring analysis only when explicitly desired, review every archive or unsubscribe action before execution, and ensure learned style data and saved templates can be deleted. <br>
Risk: Reply drafts based on personal email history may contain incorrect, over-personalized, or unintended content. <br>
Mitigation: Review every draft in full before sending and require explicit approval for each outbound message. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AGIstack/email-autopilot-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries, ranked lists, reply drafts, briefing text, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mailbox and sent-mail context; outbound sends and unsubscribe actions are described as user-approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
