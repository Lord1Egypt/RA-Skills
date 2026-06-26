## Description: <br>
Analyze and optimize cloud costs across AWS, Azure, and GCP. Use when evaluating cloud spending, identifying cost optimization opportunities, analyzing cloud bills, rightsizing instances, finding unused resources, or building cloud cost reports for management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, FinOps teams, and finance stakeholders use this skill to analyze AWS, Azure, or GCP spending, identify waste, and produce cloud cost optimization reports with savings estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends cloud provider credentials and billing data to a third-party API. <br>
Mitigation: Use dedicated least-privilege, preferably temporary read-only credentials limited to billing and cost visibility, and install only after confirming ToolWeb's billing, privacy, and data-handling terms. <br>
Risk: Credential exposure could affect AWS, Azure, or GCP billing and cost data. <br>
Mitigation: Never provide root or admin credentials; rotate or revoke the credentials immediately after analysis. <br>
Risk: The security scan reports incomplete consent and data-handling disclosures. <br>
Mitigation: Require explicit user approval before submitting credentials or billing data to the ToolWeb API. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/finopsy-cloud-finops) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>
- [Finopsy API endpoint](https://portal.toolweb.in/apis/tools/finopsy) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, JSON request examples, and structured cloud cost analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces provider-specific cost breakdowns, trend summaries, optimization recommendations, unused resource findings, and estimated savings when the ToolWeb API call succeeds.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
