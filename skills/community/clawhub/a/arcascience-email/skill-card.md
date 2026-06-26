## Description: <br>
Email assistant for Romain at ArcaScience that reads and triages Gmail messages, drafts context-aware replies using ArcaScience pharma sales materials, and suggests relevant attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atomus42](https://clawhub.ai/user/atomus42) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business development and sales users managing the ArcaScience mailbox use this skill to summarize inbound email, identify messages that need replies, draft multilingual responses, and choose supporting sales attachments. It is intended for authorized management of Romain's ArcaScience email workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a corporate Gmail inbox and draft replies using confidential sales materials. <br>
Mitigation: Install only for users authorized to manage Romain's ArcaScience mailbox and related sales content. <br>
Risk: Automated daily email drafting can process recent mailbox content on a schedule. <br>
Mitigation: Confirm whether the daily cron job is active, make it easy to disable, and review where drafts or logs are retained. <br>
Risk: The skill may attach sales, proposal, contract, or confidentiality materials to outgoing messages. <br>
Mitigation: Keep the explicit human confirmation requirement for every sent email and attachment, and review attachment choices before sending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/atomus42/arcascience-email) <br>
- [ArcaScience Company Context and Positioning](references/arcascience-context.md) <br>
- [ArcaScience Sales Package - Platform and Product Reference](references/sales-package-platform.md) <br>
- [ArcaScience Sales Package - Client Proposals and BRA Analysis](references/sales-package-proposals.md) <br>
- [ArcaScience Sales Package - Buyer Personae Analysis](references/sales-package-personae.md) <br>
- [ArcaScience Sales Package - Operations and Contracts](references/sales-package-operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown summaries, draft email text, attachment recommendations, and explicit-send guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before sending email or attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
