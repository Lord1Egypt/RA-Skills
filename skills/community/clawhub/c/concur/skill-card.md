## Description:

This skill should be used when the user asks about SAP Concur through the concur-mcp tools — expense reports, expenses, available (unassigned) card transactions and e-receipts, receipt images, or Concur Travel trips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to review their own SAP Concur expense reports, card transactions, receipts, and travel details, and to make requested expense changes through confirmation-gated actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive expense and travel records from the signed-in Concur account.

Mitigation: Install it only in a trusted environment and confirm its access fits the intended account and task.

Risk: Some expense, receipt, attendee, and itinerary actions can be permanent, one-way, or send email.

Mitigation: Review the complete preview and get the user's explicit confirmation before using its confirmation token; take extra care with irreversible actions.

Risk: The skill relies on an unofficial interface that may stop working when Concur changes its web application.

Mitigation: Check the returned result after changes; if the change succeeded but verification failed, re-read the record rather than repeating the write.

## Reference(s):

- [Project repository (linked in the skill documentation)](https://github.com/chrischall/concur-mcp)
- [npm package](https://www.npmjs.com/package/@chrischall/concur-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language summaries, explanations, and write previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive expense and travel details returned from the signed-in user's Concur account.]

## Skill Version(s):

0.5.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
