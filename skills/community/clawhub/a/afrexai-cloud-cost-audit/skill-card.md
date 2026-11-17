## Description:

Analyze multi-cloud spend data to identify waste, rightsizing, reserved capacity savings, and a prioritized cost optimization roadmap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers, FinOps practitioners, and engineering leaders use this skill to review AWS, Azure, or GCP billing and architecture details, find cloud waste patterns, estimate savings, and plan a 90-day optimization roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide billing or architecture details that may include sensitive account, customer, topology, or business information.

Mitigation: Share only the minimum information needed for analysis and redact account IDs, credentials, customer data, internal hostnames, sensitive topology details, and confidential business information unless intentional processing is required.

Risk: Cost recommendations and savings estimates may be wrong when input data is incomplete, stale, or approximate.

Mitigation: Validate recommendations against current provider billing data, service usage, compliance needs, and workload requirements before making infrastructure or purchasing changes.

## Reference(s):

- [Cloud Cost Audit on ClawHub](https://clawhub.ai/1kalin/skills/afrexai-cloud-cost-audit)
- [AfrexAI context packs](https://afrexai-cto.github.io/context-packs/)
- [AfrexAI AI savings calculator](https://afrexai-cto.github.io/ai-revenue-calculator/)
- [AfrexAI agent setup](https://afrexai-cto.github.io/agent-setup/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with executive summary, domain breakdown, findings table, 90-day roadmap, and governance recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated savings, ROI, payback period, implementation effort, and priority rankings based on user-provided billing or architecture data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
