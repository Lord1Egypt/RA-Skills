## Description:

AI Density analyzes text for heuristic AI-generation signals and returns a 0-10 AI content grade with scores, confidence, and dimension details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content reviewers use this skill to run local, heuristic checks of whether text appears AI-generated and to inspect the dimensions behind the score. Results should be treated as rough screening signals, not proof of authorship.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic AI-authorship scores can be mistaken for proof or precise human-vs-AI contribution levels.

Mitigation: Present results as rough screening signals, include confidence and warning text, and require independent review before moderation, academic, hiring, compliance, or other consequential use.

## Reference(s):

- [AI Density ClawHub Listing](https://clawhub.ai/kaiyuelv/skills/ai-density)
- [AI Density Project Homepage](https://github.com/openclaw/ai-density)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Markdown text or Python DetectionResult data with level, score, confidence, dimension scores, warning, and processing time.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input text length is documented as 10-10000 characters; outputs are heuristic and for reference only.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
