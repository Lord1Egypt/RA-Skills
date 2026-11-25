## Description:

Use when a skill package, README or report states numbers such as "9/9 PASS", "N files", "100/100" or file paths, and you need to know whether those numbers were actually produced by running the code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers reviewing a skill package, README, or report use Claim Audit before publication or handoff to compare stated test results, file counts, scores, and listed paths with available evidence. It reports mismatches and unverifiable claims for a human to assess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because it can run package-provided code and write a results file despite its read-only description.

Mitigation: Review the execution and file-writing behavior before use and run it in an isolated environment; the partial scan leaves some referenced paths unverified.

## Reference(s):

- [Claim Audit on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/claim-audit)
- [Claim rules](references/rules.md)
- [Usage guide](references/usage.md)
- [Limitations](references/limits.md)
- [Self-check coverage](references/selfcheck.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable audit report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports matched, mismatched, or unverifiable claims; strict mode treats unverifiable claims as failures.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
