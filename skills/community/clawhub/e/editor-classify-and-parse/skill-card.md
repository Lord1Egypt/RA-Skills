## Description:

Classifies Chinese story or script input into levels -1 through 4 and extracts scene, character, dialogue, action, prop, and costume structure for downstream editing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangliujiao-tal](https://clawhub.ai/user/huangliujiao-tal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative writing agents use this skill to triage story or script drafts and produce structured metadata that routes downstream editing, consistency, dialogue, and formatting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may classify ambiguous input with low confidence, which can route downstream editing work incorrectly.

Mitigation: Review detected_level, level_confidence, and level_evidence before downstream processing; request help when confidence is below the skill's threshold.

Risk: Responses may not preserve the user's preferred language unless the calling workflow makes that expectation explicit.

Mitigation: Specify the desired response language in the calling prompt or workflow when language consistency matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Structured JSON object or concise Markdown/text analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detected level, confidence, supporting evidence, extracted script structure, and risk flags when applicable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
