## Description: <br>
Helps Gate partners query affiliate commissions, referral trading activity, team metrics, eligibility, and application status through a configured Gate MCP session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate partners use this skill to view affiliate eligibility, application status, and read-only partner performance reports, including commissions, referral trading volume, team size, and user-specific contribution summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries account-specific Gate partner data through configured API credentials. <br>
Mitigation: Install only for Gate affiliate reporting and use a least-privilege Gate API key limited to Rebate:Read. <br>
Risk: Ambiguous prompts containing "commission" could be interpreted as Gate affiliate requests. <br>
Mitigation: Confirm Gate affiliate intent before making account-specific queries for vague commission prompts. <br>
Risk: Incorrect time windows or naive aggregation can produce misleading affiliate metrics. <br>
Mitigation: Respect UTC+8 date handling, 30-day request windows, the 180-day maximum range, and the documented aggregation rules. <br>


## Reference(s): <br>
- [Gate Exchange Affiliate Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Affiliate MCP Specification](references/mcp.md) <br>
- [Gate skills homepage](https://github.com/gate/gate-skills) <br>
- [Gate affiliate portal](https://www.gate.com/referral/affiliate) <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-exchange-affiliate-staging) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown reports and concise text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gate partner data; requires a configured Gate MCP session with GATE_API_KEY and GATE_API_SECRET credentials limited to Rebate:Read.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
