## Description:

Reviews text for reasoning patterns that may resemble cognitive biases, cognitive distortions, or logical fallacies, and suggests concrete checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[troioi-vn](https://clawhub.ai/user/troioi-vn)

### License/Terms of Use:

MIT-0

## Use Case:

Readers use the skill to review drafts, messages, articles, and conversations for reasoning patterns that may resemble cognitive biases or fallacies. It quotes relevant passages and offers concrete checks without judging the author.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a benign verdict with medium confidence and notes that the scan emitted warnings; the verdict is not a guarantee of safety.

Mitigation: Review the packaged source and security guidance before installing or using the skill.

Risk: The security guidance notes an unresolved mismatch between the stated purpose and the reported public catalog.

Mitigation: Check that the packaged skill and the catalog it consults match the intended release before use.

Risk: Runtime permission enforcement is unknown.

Mitigation: Limit the agent's access to what is needed to review the supplied text and retrieve the public catalog.

## Reference(s):

- [Bias Lens on ClawHub](https://clawhub.ai/troioi-vn/skills/bias-lens)
- [Public bias catalog](https://tarot.catarchy.space/biases/)
- [Catalog API documentation](https://tarot.catarchy.space/biases/api/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with quoted passages and concrete checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports possible patterns, not diagnoses or judgments about the author; no findings is a valid result, with at most five main findings per speaker.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
