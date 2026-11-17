## Description:

DealCenter helps an agent read customer account, deal, contact, activity, and document records for context and write confirmed updates back to customer files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[summerzb](https://clawhub.ai/user/summerzb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales-support agents use this skill when a customer-specific task benefits from prior DealCenter records, such as preparing follow-up messages, visit plans, proposals, or account summaries. The skill may also record customer, contact, deal, activity, or document updates when the user explicitly asks for that action or confirms a proposed update.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved write actions can create or update persistent customer, contact, deal, activity, or document records.

Mitigation: Review confirmations carefully and approve writes only when the requested record change is intended.

Risk: Customer-record context may be unavailable if the DealCenter connector is not installed or authorized.

Mitigation: Connect or reauthorize the OmniMay MCP connector before relying on DealCenter records for a customer-specific answer.

## Reference(s):

- [DealCenter Skill Page](https://clawhub.ai/summerzb/skills/dealcenter)
- [DealCenter MCP Tool Contract](references/mcp-tools.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Markdown]

**Output Format:** [Markdown or plain text responses with structured DealCenter MCP tool calls when customer-record access is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads should silently degrade when records are unavailable; writes require explicit user request or confirmation and concise created/reused/pending/skipped status reporting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
