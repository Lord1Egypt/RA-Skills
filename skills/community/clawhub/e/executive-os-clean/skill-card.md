## Description: <br>
Build or operate a chief-of-staff style communications layer that merges multiple inboxes and chat sources into one prioritized digest with follow-up memory, decision tracking, recommendations, alerts, and a strict no-send boundary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyalerio](https://clawhub.ai/user/heyalerio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to consolidate email, chat, messaging, and local notes into a prioritized operating queue with follow-up and decision memory. It supports digesting, recommendations, alerts, and approval-gated external steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may review private inbox, chat, messaging, and local-note content. <br>
Mitigation: Only provide sources the user is comfortable having summarized, and treat local notes as context rather than approved external-sharing material. <br>
Risk: Recommended next steps or alerts may be wrong when communications context is incomplete or ambiguous. <br>
Mitigation: Keep recommendations concise, include uncertainty when useful, and use source gaps to identify missing context before acting. <br>
Risk: Draft creation, account changes, bookings, spending, form submissions, or message sending could affect external systems. <br>
Mitigation: Require explicit approval before any external action or state mutation, and escalate when scope, approval, policy, or reversibility is unclear. <br>


## Reference(s): <br>
- [Operating Model](references/operating-model.md) <br>
- [Registries](references/registries.md) <br>
- [Persistent Memory](references/persistent-memory.md) <br>
- [Recommendations And Alerts](references/recommendations-and-alerts.md) <br>
- [Source Heuristics](references/source-heuristics.md) <br>
- [Local Context](references/local-context.md) <br>
- [Safety](references/safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown digest with prioritized sections, concise ledgers, recommendations, alerts, and source gaps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [External actions such as sending messages, changing account state, booking, spending, or submitting forms require explicit approval.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
