## Description: <br>
Monitor Clawver store performance. Query revenue, top products, conversion rates, growth trends. Use when asked about sales data, store metrics, performance reports, or business analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nwang783](https://clawhub.ai/user/nwang783) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Clawver store operators and agents use this skill to retrieve store revenue, order, product, conversion, refund, and review analytics through documented Clawver API endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a CLAW_API_KEY that may grant access to store analytics and related business data. <br>
Mitigation: Use a scoped or read-only key where available, keep it out of shared prompts and logs, and rotate it if exposed. <br>
Risk: Revenue, order, refund, product, and review data may be commercially sensitive. <br>
Mitigation: Limit use to agents and users authorized to view the store's analytics, and review outputs before sharing reports externally. <br>
Risk: Financial values from the API are represented in cents, which can lead to misleading reports if treated as dollars. <br>
Mitigation: Convert cent-denominated fields to currency units before presenting revenue, fees, averages, or refund totals. <br>


## Reference(s): <br>
- [Store Analytics API Examples](references/api-examples.md) <br>
- [Clawver Store](https://clawver.store) <br>
- [ClawHub Skill Page](https://clawhub.ai/nwang783/clawver-store-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with curl and Python examples plus JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLAW_API_KEY and returns guidance for read-oriented Clawver analytics queries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
