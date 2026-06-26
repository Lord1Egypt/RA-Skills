## Description: <br>
Design customer service chatbot conversation flows for ecommerce — order status, returns, product recommendations, and escalation rules — that reduce ticket volume while maintaining satisfaction scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support, ecommerce, and chatbot designers use this skill to create customer-service chatbot flows for order tracking, returns, product questions, billing, cancellations, and human escalation. The skill helps teams map intents, write response logic, define handoff rules, and prepare launch quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Escalation handoffs may expose full conversation transcripts, customer details, and order context. <br>
Mitigation: Collect explicit user consent before escalation, redact sensitive fields, and share only the minimum ticket context needed by the support team. <br>
Risk: Cancellation-related flows may act on ambiguous or unverified order requests. <br>
Mitigation: Require clear order identification and customer confirmation before any cancellation-related action. <br>
Risk: Handoff data may be visible to more staff or systems than necessary. <br>
Mitigation: Restrict access to handoff data and review the skill before using it in a live support workflow. <br>


## Reference(s): <br>
- [Chatbot Designer Skill Page](https://clawhub.ai/leooooooow/chatbot-designer) <br>
- [Output Template](output-template.md) <br>
- [Intent Library](intent-library.md) <br>
- [Escalation Playbook](escalation-playbook.md) <br>
- [Quality Checklist](quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance, templates, checklists, and conversation-flow outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include intent maps, escalation logic, response copy, KPI recommendations, and pre-launch review checklists.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
