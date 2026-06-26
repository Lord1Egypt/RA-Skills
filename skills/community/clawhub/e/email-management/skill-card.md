## Description: <br>
Triage inbox email, draft clear replies, and manage follow-ups with priority routing, commitment tracking, and reusable templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to triage provided email text, prepare context-aware draft replies, and track response commitments without connecting directly to mailbox APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email content and workflow notes may contain sensitive information if stored locally. <br>
Mitigation: Keep secrets, credentials, full payment details, and raw email dumps out of ~/email-management/; store only durable preferences, decisions, and follow-up metadata. <br>
Risk: Draft, forwarding, mailbox-rule, reminder, or digest actions could affect external communication if approved without review. <br>
Mitigation: Review proposed send, forward, mailbox-rule, reminder, and digest actions before approving them, and keep activation explicit-only or scoped to selected projects/accounts when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/email-management) <br>
- [Skill Homepage](https://clawic.com/skills/email-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with triage summaries, draft replies, follow-up records, and optional shell setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only by default; stores durable preferences and workflow notes under ~/email-management/ when approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
