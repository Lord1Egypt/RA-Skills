## Description:

Build or operate a chief-of-staff style communications layer that merges multiple inboxes and chat sources into one prioritized digest with follow-up memory, decision tracking, recommendations, alerts, and a strict no-send boundary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyalerio](https://clawhub.ai/user/heyalerio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn email, chat, messaging, and local notes into one prioritized operating queue with reply needs, pending decisions, follow-ups, low-signal items, and source gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive inbox, chat, and local-note content.

Mitigation: Use it only with sources the user intends to expose to the agent and avoid sharing local notes externally unless explicitly approved.

Risk: Recommended next steps could lead to external communication, account changes, bookings, forms, spending, or other mutations.

Mitigation: Keep the explicit approval boundary for sending messages, changing accounts, spending money, mutating external systems, or confirming real-world actions.

Risk: Unread state or incomplete context can cause over-prioritization or misleading urgency.

Mitigation: Treat unread state as weak evidence, include source gaps, use confidence where useful, and escalate when policy, scope, approval, or reversibility is unclear.

## Reference(s):

- [Executive OS ClawHub page](https://clawhub.ai/heyalerio/skills/executive-os-clean)
- [Operating Model](artifact/references/operating-model.md)
- [Registries](artifact/references/registries.md)
- [Persistent Memory](artifact/references/persistent-memory.md)
- [Recommendations And Alerts](artifact/references/recommendations-and-alerts.md)
- [Safety](artifact/references/safety.md)
- [Source Heuristics](artifact/references/source-heuristics.md)
- [Local Context](artifact/references/local-context.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown digest with concise sections, recommended next steps, and optional follow-up or decision ledger entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external messages, posts, sends, or system mutations without explicit approval.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
