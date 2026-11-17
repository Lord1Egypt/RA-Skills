## Description:

Evaluates Spanish-language visual hooks from first-second screenshots or videos using FÓRMULA 100K criteria and returns a scored diagnostic with practical recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to evaluate the first second of Spanish-language social videos or thumbnails, identify weaknesses in visual hooks, and receive concrete revisions before publishing. When a full video is provided, it can add an optional Higgsfield Virality Predictor reading after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full video may be uploaded to the external Higgsfield predictor during the optional quantitative analysis step.

Mitigation: Confirm user consent before upload and avoid using sensitive unpublished media unless that matches the user's workflow.

Risk: The diagnostic may give incorrect or overconfident creative advice if the screenshot is low quality, lacks context, or is not from the first second.

Mitigation: Request missing context or a clearer first-second capture before scoring, and do not infer visual elements that are not visible.

## Reference(s):

- [Skill release page](https://clawhub.ai/formula100k/skills/evaluador-ganchos-formula100k)
- [Evaluation criteria](artifact/criterios.md)
- [Diagnostic output template](artifact/output-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic with a numeric score, structured findings, prioritized recommendations, and optional Virality Predictor results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-neutral prose; may provide a markdown file for long reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
