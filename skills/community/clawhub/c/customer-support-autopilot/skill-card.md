## Description: <br>
Classify customer support tickets, draft accurate responses, suggest macros, and route escalations based on risk, SLA, and business impact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support teams use this skill to triage incoming customer tickets, draft policy-aware responses, recommend macros, and route cases to the right escalation tier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts may include inaccurate SLA, refund, billing, or policy statements. <br>
Mitigation: Review drafts before sending and verify policy-specific statements against current support references. <br>
Risk: Customer tickets may contain sensitive personal or account information. <br>
Mitigation: Avoid including unnecessary sensitive customer information in prompts and do not disclose sensitive internal information. <br>
Risk: Legal, security, billing, fraud, abuse, or other regulated cases may require higher-touch handling. <br>
Mitigation: Escalate high-risk cases immediately according to approved L1/L2/L3 routing and incident contacts. <br>


## Reference(s): <br>
- [Customer Support Autopilot on ClawHub](https://clawhub.ai/anugotta/customer-support-autopilot) <br>
- [Publisher profile: anugotta](https://clawhub.ai/user/anugotta) <br>
- [Setup](setup.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or structured text containing category, severity, draft response, escalation recommendation, SLA target, and required follow-up.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent drafts should be reviewed against current support policy before sending to customers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
