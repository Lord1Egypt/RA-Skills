## Description:

Classify customer support tickets, draft accurate responses, suggest macros, and route escalations based on risk, SLA, and business impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and customer-facing agents use this skill to triage tickets, draft policy-grounded replies, recommend macros, and route escalations for risky or urgent cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted support responses may be wrong if required support policies, SLA rules, or escalation criteria are missing or stale.

Mitigation: Provide current support policies, SLA definitions, escalation rules, tone guidance, and prohibited claims before use.

Risk: Legal, security, billing, fraud, abuse, or other high-risk cases may need judgment beyond automated drafting.

Mitigation: Keep a human review and escalation step for high-risk cases before sending responses or taking action.

Risk: Ticket data and support policy context can contain sensitive information.

Mitigation: Provide only the ticket data and policy references needed for the task and avoid disclosing sensitive internal information in generated replies.

## Reference(s):

- [Customer Support Autopilot on ClawHub](https://clawhub.ai/anugotta/skills/customer-support-autopilot)
- [setup.md](artifact/setup.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text containing ticket category, severity, draft response, escalation recommendation, SLA target, and follow-up notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires relevant support policies, escalation rules, SLA definitions, tone guidance, and prohibited claims to produce grounded recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
