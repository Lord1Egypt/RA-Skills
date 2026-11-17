## Description:

Compares LLM API prices across major providers and helps estimate or recommend lower-cost models for common tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare LLM provider and model pricing, estimate token-based API costs, and choose lower-cost models for chat, coding, writing, or reasoning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Git install is unpinned, so users may install code that differs from the reviewed artifact.

Mitigation: Install from a trusted, pinned release or commit and review the package before use.

Risk: The description advertises spending tracker commands that the package does not implement.

Mitigation: Use implemented commands only, such as list, compare, recommend, and estimate, and verify functionality before relying on workflows.

Risk: API pricing can change, and static model data may become stale.

Mitigation: Confirm prices against provider billing pages before making purchasing or production routing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/api-cost-compare)
- [Project homepage](https://github.com/minirr890112-byte/api-cost-compare)
- [English README](artifact/README_EN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with CLI command examples and tabular cost comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cost estimates, provider/model recommendations, and install or run commands; pricing data should be reviewed for freshness.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
