## Description:

Helps users record and review emotion events, thoughts, predictions, and follow-ups through conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[advnljs](https://clawhub.ai/user/advnljs)

### License/Terms of Use:

MIT-0

## Use Case:

People using conversational assistants can keep a private record of emotional experiences and revisit thoughts, predictions, and changes over time. The skill can summarize recorded patterns on request while prioritizing supportive conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate when a user discusses emotions without explicitly asking to log them.

Mitigation: Review whether this activation behavior suits the user, and make the logging preference and opt-out clear.

Risk: Emotion records can contain sensitive personal information.

Mitigation: Use only a private storage location the user has authorized, and do not move records to a new service without permission.

Risk: Security analysis had partial coverage because a referenced local path was unavailable.

Mitigation: Review the complete skill and resolve the missing reference before relying on the security assessment.

## Reference(s):

- [CBT Emotion Log release page](https://clawhub.ai/advnljs/skills/cbt-emotion-log)
- [Stats and review definitions](artifact/references/analysis.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis]

**Output Format:** [Conversational text and structured emotion records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional record fields; replies use the user's language.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
