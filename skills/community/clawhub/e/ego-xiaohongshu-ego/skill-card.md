## Description:

Publishes one Xiaohongshu video or image-text note through the logged-in creator interface using Ego Lite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and publish one video or image-text note to Xiaohongshu from a logged-in creator account. The agent checks the account and plan, and publishing requires explicit --yes approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A faulty creator-account check can allow uploads and publishing through the wrong signed-in account.

Mitigation: Use a version that refuses uploads and publishing when the creator account cannot be verified. Do not treat --expect-account as proof; confirm the creator account, selected media, text, and audience before approving --yes.

## Reference(s):

- [Inputs and options](references/inputs.md)
- [Login and account checks](references/login.md)
- [Video publishing flow](references/publish-flow.md)
- [Image-text publishing flow](references/imagetext-flow.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [A publish plan or result; successful publishing returns a public note URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One note per invocation; video or 1–18 images. Uploading and publishing require --yes.]

## Skill Version(s):

0.2.0 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
