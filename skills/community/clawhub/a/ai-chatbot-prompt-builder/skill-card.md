## Description:

Creates structured prompt assets for building business chatbot system prompts, personas, guardrails, and FAQ training datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitflopez](https://clawhub.ai/user/gitflopez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agencies, product teams, and business operators use this skill to generate chatbot launch materials for support, sales, onboarding, internal help desks, and knowledge base assistants. The generated assets help define bot behavior, brand voice, escalation handling, and structured FAQ data before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chatbot personas can imply a fictional human identity or obscure that the assistant is AI-powered.

Mitigation: Keep the chatbot's AI identity clear to end users and remove fake human backstories before deployment.

Risk: FAQ, fine-tuning, or RAG workflows may expose private customer data, regulated records, or confidential support tickets.

Mitigation: Use approved source material, remove sensitive data, and obtain the right approvals before uploading data to third-party systems.

Risk: Chatbots in regulated or sensitive industries may produce advice or handling guidance that requires review.

Mitigation: Review generated guardrails with the appropriate legal, compliance, or subject-matter experts and use human escalation for high-risk cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitflopez/skills/ai-chatbot-prompt-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown prompt outputs with system prompt, persona, guardrail, and JSONL, CSV, Markdown, or plain-text FAQ dataset sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces four prompt-guided deliverables, including chatbot instructions, brand voice material, safety rules, escalation matrices, and structured Q&A training examples.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
