## Description:

Drafts external emails for human approval before sending, with an approval-first workflow for support, competition, business, and partnership communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefanferreira](https://clawhub.ai/user/stefanferreira)

### License/Terms of Use:

MIT-0

## Use Case:

External-facing agents and operators use this skill to draft emails for support tickets, competition entries, business inquiries, and partnership discussions, then send only after explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured recipients, sender identity, workspace paths, or email delivery setup may be incorrect for the deployment environment.

Mitigation: Review those settings before use and keep the explicit human approval step in place before any external email is sent.

Risk: The CSV audit log can reveal contacted parties and communication purpose.

Mitigation: Store the audit log with access controls appropriate for sensitive operational records and review retention needs before deployment.

Risk: Ambiguous approval language could lead to sending an email before the approver intended it.

Mitigation: Require one of the explicit approval phrases defined by the workflow and resubmit edited drafts for approval before sending.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with email draft templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit human approval before sending; records sent-email activity in an audit log when used as written.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
