## Description: <br>
Provides a lightweight FAQ-based customer support scaffold with webhook replies, CSV FAQ loading, template responses, and escalation to human support or ticketing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xianji520](https://clawhub.ai/user/xianji520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to scaffold a simple customer-support bot that answers common questions from a CSV FAQ, exposes a webhook endpoint, and routes low-confidence messages to human follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The development server can be exposed publicly or run with Flask debug mode enabled. <br>
Mitigation: Disable debug mode and avoid exposing the development server before connecting the skill to real customer channels. <br>
Risk: Automatic replies or ticket creation can send incorrect responses or create unintended support actions. <br>
Mitigation: Run staging tests and require explicit confirmation before enabling automatic replies or live ticket creation. <br>
Risk: Channel credentials may be mishandled during integration. <br>
Mitigation: Keep channel credentials in environment variables or a secrets manager and grant only the permissions needed for message handling and ticket creation. <br>


## Reference(s): <br>
- [Integration Guides](references/integration-guides.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xianji520/auto-customer-support) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, JSON response examples, shell commands, CSV data, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local Flask scaffold for FAQ retrieval, webhook handling, and escalation stubs; production channels require operator review and credential configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
