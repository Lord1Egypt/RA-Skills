## Description:

Dialogue Next Steps guides an agent to answer first, then append up to five numbered next-step options for beginner, conceptual, underspecified, or explicitly plan-seeking requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqfcyily](https://clawhub.ai/user/sqfcyily)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn single Q&A responses into guided conversations by answering first, then adding concise numbered next-step options when the request is beginner-level, conceptual, underspecified, or explicitly asks for a plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Responses may become longer or feel over-guided when next steps are appended.

Mitigation: Use the documented gate and suggestion threshold: skip next steps for trivial, advanced execution-ready, or explicit no-suggestion requests, and cap lists at five items.

## Reference(s):

- [Dialogue Next Steps on ClawHub](https://clawhub.ai/sqfcyily/skills/dialogue-next-steps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown response with an optional numbered next-steps list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers first, then appends up to five localized next-step options when the gate applies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
