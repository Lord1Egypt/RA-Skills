## Description:

French Business Analyser gives autonomous B2B agents real-time French business, supplier-risk, invoice, and registry checks from official sources through an MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vannelier](https://clawhub.ai/user/vannelier)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to verify French suppliers, invoices, VAT details, liens, certifications, director risk, and due-diligence signals before payments, onboarding, procurement, or portfolio monitoring.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: French company identifiers and optional invoice text or IBAN data may be sent to the hosted MCP service and disclosed server-side providers.

Mitigation: Use the hosted service only for data you are comfortable submitting, or self-host the service for confidential documents and infrastructure control.

Risk: Paid tools can create costs and submit business data if an automated workflow calls them without approval.

Mitigation: Confirm the MCP client enforces the documented consent prompt and displays the cost before any paid call.

Risk: A pay verdict is a risk signal, not a solvency guarantee, and some confidential procedures or delayed registry publications may be unavailable.

Mitigation: Treat verdicts as decision support, review returned flags and timestamps, and escalate hold, block, incomplete, or high-value payment cases to a human reviewer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vannelier/skills/french-business-analyser)
- [Source code and documentation](https://github.com/Vannelier/MCP-business-checker)
- [Hosted MCP service](https://mcp-business-checker-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured text from MCP tool calls, with JSON configuration snippets for setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces supplier-risk verdicts, invoice extraction and compliance checks, registry lookup summaries, comparative rankings, and recommended actions.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
