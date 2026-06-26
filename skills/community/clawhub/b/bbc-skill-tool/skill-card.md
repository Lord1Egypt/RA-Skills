## Description: <br>
Builds, manages, and troubleshoots WhatsApp bots using the BuilderBot Cloud (BBC) MCP Tool v2.0, with guidance for business bot flows, deployment validation, recovery, and safety gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leifermendez](https://clawhub.ai/user/leifermendez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and business operators use this skill to create, manage, validate, deploy, and troubleshoot BuilderBot Cloud WhatsApp bots for appointments, customer support, lead capture, content delivery, and human handoff workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WhatsApp bot workflows may collect customer names, contact details, appointment requests, order data, or conversation context. <br>
Mitigation: Add user-facing privacy notices, collect only necessary data, redact sensitive conversation content, and protect credentials before production use. <br>
Risk: Webhook, CRM, scraping, and handoff examples can send data to external endpoints. <br>
Mitigation: Use trusted endpoints, validate webhook destinations, and avoid sending sensitive data unless the business has an approved data handling process. <br>
Risk: Deployment or deletion actions can change live bot behavior or remove configured flows. <br>
Mitigation: Require explicit user confirmation before deployment or deletion and verify state after every mutating action. <br>


## Reference(s): <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Advanced Patterns](artifact/advanced-patterns.md) <br>
- [Vertical Templates](artifact/verticals.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/leifermendez/bbc-skill-tool) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, API calls] <br>
**Output Format:** [Markdown guidance with structured bot plans, validation reports, and BuilderBot Cloud tool-call instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes verification after mutations, explicit confirmation before destructive actions, recovery guidance, and validation before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
