## Description:

Bias Audit is a decision-framing agent skill for surfacing bias before it hardens, using a disciplined protocol and fixed output contract instead of a generic answer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarkchenkai](https://clawhub.ai/user/clarkchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Bias Audit to inspect loaded or emotionally slanted decision framing, identify bias signals, rewrite questions neutrally, surface missing evidence, and define decision criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate broadly on loaded or poorly structured decisions and steer a conversation into a fixed bias-review format.

Mitigation: Use explicit instructions when a conversation should not receive bias-audit treatment.

Risk: A framing audit can highlight likely distortions but does not replace domain evidence or expert review.

Mitigation: Treat the audit as a decision-framing aid and verify recommendations against relevant evidence, baselines, and criteria.

## Reference(s):

- [Audit Rules](references/audit-rules.md)
- [Bias Patterns](references/bias-patterns.md)
- [Kahneman Reference](references/kahneman.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with six labeled sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always ends with Original Framing, Bias Signals, Neutral Reframe, Missing Evidence, Decision Criteria, and Recommended Next Step.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
