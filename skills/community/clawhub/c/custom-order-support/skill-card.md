## Description: <br>
Manage customer expectations, order changes, and post-purchase support for long-lead custom products such as engraved necklaces, custom pet portraits, and personalized gifts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RIJOYAI](https://clawhub.ai/user/RIJOYAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support agents and DTC store operators use this skill to draft clear, empathetic post-purchase responses for custom-order status checks, modification requests, quality complaints, and return eligibility questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proactive email, SMS, or loyalty follow-up suggestions may be used without customer consent or channel preference checks. <br>
Mitigation: Confirm customer opt-in and channel preferences, honor unsubscribe rules, and share only the minimum necessary order data before enabling those workflows. <br>
Risk: Drafted responses may overcommit the business to refunds, remakes, reships, rush orders, or order changes. <br>
Mitigation: Require human approval before promising refunds, remakes, reships, rush timelines, or changes to an existing custom order. <br>


## Reference(s): <br>
- [Custom product FAQ](references/faq.md) <br>
- [Custom product post-purchase and change policy](references/policy.md) <br>
- [Rijoy](https://www.rijoy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured support sections and optional ETA command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [ETA calculations can use scripts/calculate_eta.py when order dates and production or shipping parameters are available.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
