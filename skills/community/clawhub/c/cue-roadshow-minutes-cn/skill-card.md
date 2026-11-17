## Description:

Reads roadshow or research minutes into an eight-item verbatim summary with source anchors and spoken-claim labels, while leaving ratings and price targets for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and investors use this skill to extract and compare statements in roadshow or research minutes, retain source locations, and identify missing information. It keeps investment ratings, target prices, and directional judgments for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential minutes and attachments may be sent to Cue when optional integrations are used.

Mitigation: Before sending attachments, confirm that external processing and its retention terms are acceptable.

Risk: Supplying the optional API key to an unverified destination could expose credentials.

Mitigation: Verify the HTTPS recipient before supplying the key, and keep the key out of chat.

Risk: Optional companion skills have behavior that was not assessed with this release.

Mitigation: Review companion skills separately and prefer reviewed installation revisions.

## Reference(s):

- [Oral claims reference](artifact/references/oral-claims.md)
- [Cue data integration setup](https://cuecue.cn/hub/mcp)
- [Cue document parsing setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown minutes card with five sections and eight source-anchored items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps figures verbatim, labels spoken claims as unchecked against disclosures, names missing items, and marks investment judgments for human review.]

## Skill Version(s):

0.1.1 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
