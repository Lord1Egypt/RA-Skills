## Description:

AI Detection Tool - Detect AI-generated text with multiple analysis methods including perplexity analysis, burstiness detection, readability scoring, and AI fingerprint detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze pasted or file-based text for signals associated with AI-generated writing. It returns an advisory AI probability, component scores, detected writing patterns, and plain-language interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-detection scores can be wrong and should not be treated as proof of authorship.

Mitigation: Present results as advisory, include confidence and component signals, and require human review before consequential decisions.

Risk: Users may provide confidential, regulated, or sensitive text for analysis.

Mitigation: Run analysis locally and advise users not to submit secrets, regulated personal data, or confidential documents unless intended.

## Reference(s):

- [AI Writing Patterns Reference](references/ai_patterns.md)
- [Detector AI ClawHub Release](https://clawhub.ai/openlark/skills/detector-ai)
- [OpenLark Publisher Profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown summary with optional JSON detector output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local advisory analysis with probability, verdict, confidence, text statistics, and component scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
