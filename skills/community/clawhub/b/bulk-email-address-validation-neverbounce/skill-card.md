## Description:

Bulk verifies up to 1,000 email addresses through AgentPMT-hosted NeverBounce tool calls using the user's connected NeverBounce API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to validate bulk contact lists, clean marketing or CRM data, and reduce email bounce risk before campaigns, imports, migrations, outreach, or database hygiene workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email lists may be sent to external AgentPMT or NeverBounce services.

Mitigation: Confirm authorization to submit the addresses, limit inputs to the minimum needed, and avoid sending sensitive contact lists without appropriate approval.

Risk: The skill relies on setup routes and live schema details that may change.

Mitigation: Review or pin the setup skills and fetch live schema or instructions before new production integrations.

Risk: Each submitted email can consume verification credits.

Mitigation: Check expected cost before large batches and split lists deliberately within the documented 1,000-address request limit.

Risk: Broad prompts may invoke bulk validation unintentionally.

Mitigation: Use explicit activation only when bulk email validation through AgentPMT/NeverBounce is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/bulk-email-address-validation-neverbounce)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/bulk-email-address-validation-neverbounce)
- [Action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, configuration]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces validation guidance and invocation shapes for the verify action; tool responses may include per-email results, summary counts, and job status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
