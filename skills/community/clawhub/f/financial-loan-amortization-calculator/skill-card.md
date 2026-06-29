## Description: <br>
Financial Loan Amortization Calculator supports loan and mortgage calculations, including payment estimates, amortization schedules, loan comparisons, affordability analysis, refinance break-even checks, payoff acceleration modeling, and interest calculations through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate loan payments, generate amortization schedules, compare lending scenarios, estimate affordability, evaluate refinancing, and model early payoff strategies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loan and affordability inputs may include sensitive financial data sent to AgentPMT. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid including unnecessary personal identifiers. <br>
Risk: CSV amortization exports are stored in cloud storage and exposed through a signed URL until expiration. <br>
Mitigation: Leave store_schedule_file disabled unless a downloadable schedule is required, and use the shortest practical expiration. <br>


## Reference(s): <br>
- [Financial Loan Amortization Calculator on ClawHub](https://clawhub.ai/agentpmt/skills/financial-loan-amortization-calculator) <br>
- [AgentPMT Financial Loan Calculator](https://www.agentpmt.com/marketplace/financial-loan-calculator) <br>
- [Generated action schema](schema.md) <br>
- [AgentPMT account and API setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and structured tool response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can describe CSV schedule export metadata when store_schedule_file is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
