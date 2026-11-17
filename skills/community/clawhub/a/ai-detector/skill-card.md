## Description:

Detect whether text is human-written, AI-generated, AI-humanized, or lightly edited.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattc95](https://clawhub.ai/user/mattc95)

### License/Terms of Use:

MIT-0

## Use Case:

External users, reviewers, and developers use this skill to classify submitted text as likely human-written, AI-generated, AI-humanized, or lightly edited and to review supporting probability scores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided text is sent to GPTHumanizer's external detection service.

Mitigation: Do not submit secrets, private customer data, regulated records, or unpublished confidential material unless the organization has approved that service.

Risk: AI-detection results are probabilistic and may be less reliable for short, mixed, or heavily edited text.

Mitigation: Present the classification with supporting probabilities and avoid treating the result as definitive proof.

Risk: The external API can fail, time out, or return incomplete results.

Mitigation: Clearly report incomplete detection rather than fabricating or overconfidently inferring a classification.

## Reference(s):

- [AI Detector ClawHub Page](https://clawhub.ai/mattc95/skills/ai-detector)
- [GPTHumanizer Homepage](https://www.gpthumanizer.ai/)
- [GPTHumanizer Detection API](https://detect.gpthumanizer.ai/api/detect_ai)
- [API Reference](api.md)
- [Examples](examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown summary with classification label and probability values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detection results are probabilistic and may include the original input text when returned by the service.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
