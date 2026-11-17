## Description:

Turns one mainland Chinese insurance policy into an eight-item verbatim summary with source anchors, marks missing terms, and leaves payout or coverage judgments for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use it to read one Chinese insurance policy and locate exact wording on coverage, exclusions, amounts, waiting periods, claims deadlines, cancellation, and disclosure. It identifies missing information and leaves coverage decisions and payout estimates for human review.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: Optional external PDF processing may share private policy documents with a companion service; its live behavior, recipients, and retention were not verified.

Mitigation: For private policies, use supplied text unless sharing is authorized. Before enabling parsing, confirm what is sent, who receives it, and retention terms.

Risk: Optional credentials and integrations can expose data if sent to an unintended destination or if unnecessary components are enabled.

Mitigation: Verify the credential destination and install only the components you need from reviewed versions.

## Reference(s):

- [Insurance layers and source anchors](artifact/references/insurance-layers.md)
- [Cue MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown policy summary with verbatim quotes, source anchors, missing-item notes, and human-review flags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight policy topics; amounts and periods remain verbatim; payout estimates and coverage decisions are left for human review.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact/SKILL.md frontmatter, artifact/CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
