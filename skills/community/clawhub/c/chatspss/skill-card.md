## Description:

Runs 22 common statistical analyses on user-provided datasets and presents complete Markdown result tables, while identifying advanced methods outside the public release's scope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessepwj](https://clawhub.ai/user/jessepwj)

### License/Terms of Use:

MIT-0

## Use Case:

External users can analyze CSV, Excel, SPSS, or Stata datasets with common statistical methods and receive complete result tables with explanations. The skill identifies advanced methods outside its public scope and describes those limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis results can reproduce dataset labels and text in the conversation.

Mitigation: Select only datasets intended for analysis and review the generated output before sharing it.

Risk: Optional website behavior and installed dependency internals are outside the bundled-code review.

Mitigation: Use an isolated Python environment and review any external service or dependency behavior relevant to your use.

## Reference(s):

- [Longitudinal, panel, and spatial methods scope](artifact/references/longitudinal-panel-spatial.md)
- [Latent and mechanism models scope](artifact/references/latent-and-mechanism-models.md)
- [Advanced prediction and delivery scope](artifact/references/advanced-prediction-and-delivery.md)
- [ChatSPSS official website](https://chatspss.cn/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown result tables with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows complete result tables before interpretation.]

## Skill Version(s):

0.2.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
