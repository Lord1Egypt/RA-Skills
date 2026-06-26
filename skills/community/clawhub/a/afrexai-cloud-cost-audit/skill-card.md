## Description: <br>
Analyze multi-cloud spend data to identify waste, rightsizing, reserved instance savings, and a prioritized 90-day cost optimization roadmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cloud, platform, and finance teams use this skill to analyze AWS, Azure, or GCP spend data and produce prioritized optimization findings, savings estimates, and an execution roadmap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud billing exports, cost screenshots, and architecture descriptions can contain secrets, account identifiers, customer information, internal hostnames, or sensitive infrastructure details. <br>
Mitigation: Provide only the minimum necessary data and redact secrets, account IDs where possible, customer information, internal hostnames, and sensitive architecture details before use. <br>
Risk: Savings estimates and benchmark comparisons may be inaccurate when submitted spend or architecture data is incomplete or approximate. <br>
Mitigation: Review recommendations against provider billing data, operational requirements, and purchasing constraints before changing infrastructure or commitments. <br>


## Reference(s): <br>
- [Cloud Cost Audit on ClawHub](https://clawhub.ai/1kalin/afrexai-cloud-cost-audit) <br>
- [AfrexAI context packs](https://afrexai-cto.github.io/context-packs/) <br>
- [AfrexAI AI savings calculator](https://afrexai-cto.github.io/ai-revenue-calculator/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with executive summary, domain breakdown, findings table, savings estimates, and 90-day roadmap] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on user-provided billing exports, cost summaries, screenshots, architecture descriptions, or stack details; estimates should be reviewed before action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
