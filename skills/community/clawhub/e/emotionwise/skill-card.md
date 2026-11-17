## Description:

Analyze text for emotions and sarcasm using the EmotionWise API (28 labels, EN/ES).

This skill is ready for commercial/non-commercial use.

## Publisher:

[timexicali](https://clawhub.ai/user/timexicali)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to analyze text for emotional labels, confidence scores, sarcasm, and short practical interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted text is sent to an external EmotionWise service for analysis.

Mitigation: Avoid submitting secrets, regulated personal data, or confidential business text unless EmotionWise's data handling is acceptable for the use case.

Risk: The skill requires an EmotionWise API key.

Mitigation: Keep EMOTIONWISE_API_KEY private and install only from the reviewed ClawHub version or a pinned release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timexicali/skills/emotionwise)
- [EmotionWise homepage](https://emotionwise.ai)
- [EmotionWise emotion detector endpoint](https://api.emotionwise.ai/api/v1/tools/emotion-detector)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary of top emotions, confidence scores, sarcasm result, and practical interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EMOTIONWISE_API_KEY and sends submitted text to the EmotionWise API.]

## Skill Version(s):

0.1.2 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
