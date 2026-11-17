## Description:

Analyze financial text sentiment using FinBERT or an LLM, returning positive, negative, or neutral sentiment with a numeric score and brief reasoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to classify financial news or market text sentiment, obtain a score from -1.0 to 1.0, and optionally update stored news records with the analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database update helpers can modify news sentiment records and should be treated as administrative database capabilities.

Mitigation: Use the skill only in a contained environment with a database you are comfortable letting it modify.

Risk: Model loading may rely on unpinned or runtime network behavior.

Mitigation: Use a pre-cached, pinned, verified model and disable runtime model downloads where possible.

Risk: Security evidence marks the release as suspicious and recommends review before installation.

Mitigation: Review the skill and its database/model configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouzhonglu8-png/skills/alphaear-sentiment)
- [ClawHub publisher profile](https://clawhub.ai/user/zhouzhonglu8-png)

## Skill Output:

**Output Type(s):** [text, JSON, code, configuration, guidance]

**Output Format:** [JSON-like sentiment result with score, label, and reason, plus optional database update effects and agent guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores use a -1.0 to 1.0 range; labels are positive, negative, neutral, or error.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
