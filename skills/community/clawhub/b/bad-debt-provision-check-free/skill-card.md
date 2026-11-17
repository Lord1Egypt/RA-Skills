## Description:

坏账准备计提表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting staff use this skill during month-end close, reconciliation, or audit preparation to locally check bad-debt provision tables. It recomputes provision amounts and totals, detects duplicate or blank fields, and returns findings with source-line evidence when the input table is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Node.js command over accounting table data supplied by the user.

Mitigation: Run it only in an environment where executing the packaged command is acceptable, and review the input data handling expectations before use.

Risk: The free release intentionally omits several checks listed by the artifact, so a clean result is not a full accounting review.

Mitigation: Treat output as a scoped consistency check and separately review withheld or out-of-scope accounting policy questions.

Risk: The interface and diagnostic text are Chinese-first, which may affect review by non-Chinese-speaking operators.

Mitigation: Use reviewers who can understand the Chinese output or translate results before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bad-debt-provision-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON reports with line-cited findings, executed-check lists, withheld-check lists, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with the packaged Node.js checker, uses a free subset of declared checks, and requires an input table with recognizable headers.]

## Skill Version(s):

1.0.60 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
