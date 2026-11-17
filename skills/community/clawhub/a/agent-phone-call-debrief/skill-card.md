## Description:

Debrief after an AI agent phone call by comparing outcome to goal, capturing commitments, flagging escalations, and producing follow-up tasks and CRM-ready notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruti3](https://clawhub.ai/user/ruti3)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-service, booking, support, and operations users use this skill after inbound, outbound, or callback AI phone calls to turn transcripts or summaries into grounded debriefs, follow-up tasks, and CRM-ready notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted call transcripts or summaries may contain sensitive personal, medical, legal, financial, or compliance-related information.

Mitigation: Use only the call details needed for the debrief and route sensitive calls for human review.

Risk: Generated CRM or ticket notes could preserve uncertain or unsupported details from incomplete call artifacts.

Mitigation: Review outputs before copying them into a CRM or ticket system and keep uncertain extractions marked with [unclear] or [verify].

## Reference(s):

- [Agent Phone Call Debrief on ClawHub](https://clawhub.ai/ruti3/skills/agent-phone-call-debrief)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown debrief with tables, checklist follow-up tasks, and a concise CRM or ticket note.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in user-provided call transcripts, summaries, or notes; uncertain extractions are marked for verification.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
