## Description:

Design customer service chatbot conversation flows for ecommerce - order status, returns, product recommendations, and escalation rules - that reduce ticket volume while maintaining satisfaction scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce support teams and chatbot builders use this skill to design customer service chatbot flows, intent maps, escalation rules, response copy, and measurement plans for order status, returns, product questions, billing issues, and human handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends sharing full conversation transcripts during escalation, which may expose unnecessary customer data.

Mitigation: Use minimized and redacted handoff summaries unless the privacy policy, consent flow, retention rules, and support access controls explicitly allow broader transcript sharing.

Risk: Automated cancellations, refunds, replacements, return labels, and claims can affect customer accounts or orders if triggered without confirmation.

Mitigation: Require explicit customer confirmation before any account, order, refund, replacement, return-label, or claim action is executed.

Risk: Broad single-word intent triggers can route customers into order-data flows too easily.

Mitigation: Use contextual intent matching and confirmation prompts before collecting order data or initiating account-specific workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/chatbot-designer)
- [Output Template](artifact/output-template.md)
- [Intent Library](artifact/intent-library.md)
- [Escalation Playbook](artifact/escalation-playbook.md)
- [Quality Checklist](artifact/quality-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with flow templates, decision tables, checklist items, and conversation copy examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces chatbot flow design documents, intent mappings, escalation protocols, quality checklists, and response templates for ecommerce support workflows.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
