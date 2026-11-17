## Description:

AI Customer Service guides OpenClaw or Hermes agents to answer WeChat/WeCom customer support questions from a local llm-wiki knowledge base, redirect unrelated requests, and route risky or unsupported cases to human support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and developers use this skill to define customer-service behavior for WeChat, WeCom, web chat, and similar channels. It helps an agent answer company product and service questions from a curated local wiki, ask clarifying questions, redirect out-of-scope requests, and hand off cases that require human authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer replies can be incorrect or misleading if the local support wiki is missing, stale, or conflicts with current company policy.

Mitigation: Use a curated support wiki, review the schema, index, and recent log before answering, and route unsupported or uncertain cases to human support.

Risk: Raw customer personal data or private internal notes in the knowledge base can improperly influence customer-facing replies.

Mitigation: Point SUPPORT_WIKI_PATH or WIKI_PATH at a curated support knowledge base and avoid including raw personal data or private internal notes.

Risk: Refunds, payments, contracts, discounts, identity verification, and other binding decisions require authority beyond the skill.

Mitigation: Explain only published policy from the wiki and hand off cases requiring approval, verification, compensation, or binding commitments to human support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/ai-cs)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with customer-facing response examples, policy checklists, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounds customer-service answers in a local support wiki and uses human handoff for unsupported, sensitive, or authority-requiring cases.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
