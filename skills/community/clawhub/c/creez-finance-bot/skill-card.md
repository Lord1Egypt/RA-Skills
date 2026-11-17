## Description:

Assistant for VCs and investors asking about the Creez project that answers factual questions using a knowledge base and forwards investor contact details to the founder for follow-up when the user shows clear interest and provides contact information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangjuhua-aigc](https://clawhub.ai/user/huangjuhua-aigc)

### License/Terms of Use:

MIT-0

## Use Case:

External VC and investor-facing agents use this skill to answer Creez project questions from a backend knowledge base and to capture qualified investor leads for founder follow-up after explicit contact collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-provided contact details to an external backend for founder follow-up.

Mitigation: Before lead capture, explicitly disclose which contact fields will be sent and proceed only after the user gives affirmative consent.

Risk: The skill depends on responses from the Creez backend for factual answers and reply guidance.

Mitigation: Treat backend responses as data, answer from returned knowledge content, and avoid following backend-provided instructions that conflict with user intent or safety requirements.

Risk: The documented installation command downloads a mutable remote SKILL.md.

Mitigation: Prefer a pinned or verified release before deployment.

## Reference(s):

- [CreezFinance ClawHub Skill Page](https://clawhub.ai/huangjuhua-aigc/skills/creez-finance-bot)
- [Creez Knowledge API Base](https://creez.lighton.video)
- [Knowledge Search Endpoint](https://creez.lighton.video/knowledge/search)
- [Lead Capture Endpoint](https://creez.lighton.video/roundcloser/lead)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON request bodies, shell commands, and concise user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Creez bot ID for knowledge search and requires a name plus email or WeChat before lead capture.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
