## Description:

Browser Ops High Autonomy automates routine browser workflows end-to-end on approved domains and escalates for login, security, legal, payment, or blocking events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forevercrab321-svg](https://clawhub.ai/user/forevercrab321-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, support, and administrative teams use this skill to complete browser-based work such as customer support flows, email operations, CRM updates, ordinary forms, platform operations, and structured research on approved domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-autonomy browser actions can affect accounts, records, communications, and admin workflows with limited confirmation.

Mitigation: Use tightly limited approved domains, low-privilege browser sessions, and explicit confirmation before sending messages, submitting forms, changing settings or permissions, exporting data, or performing bulk or irreversible actions.

Risk: The skill may encounter login verification, security challenges, legal documents, payment actions, or unsupported domains during automated workflows.

Mitigation: Stop and return the corresponding status so a human can review the next action before the workflow continues.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forevercrab321-svg/skills/browser-ops-high-autonomy)
- [Publisher profile](https://clawhub.ai/user/forevercrab321-svg)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Machine-readable status metadata with short rationale and next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one of DONE, BLOCKED, LOGIN_REQUIRED, SECURITY_CHALLENGE, LEGAL_REVIEW_REQUIRED, PAYMENT_REVIEW_REQUIRED, or DOMAIN_NOT_ALLOWED.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
