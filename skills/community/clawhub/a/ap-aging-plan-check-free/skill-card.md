## Description:

Checks accounts payable aging and payment-plan tables by recalculating row and total relationships, detecting duplicate suppliers and blank or placeholder cells, and citing source lines for findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, treasury, and accounting users use this skill during monthly close, reconciliation, and cash-planning reviews to check AP aging and payment-plan tables before relying on them for payment scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on a clean result even though the free version omits listed AP aging and payment-plan checks.

Mitigation: Review the checks not included in the free version and perform additional financial review before using results for payment decisions.

Risk: The skill is a Chinese-language local accounting checker and may not fit teams that cannot review its terminology or output.

Mitigation: Use it only when reviewers are comfortable validating Chinese AP aging/payment-plan tables and the returned findings.

Risk: Insufficient or poorly formatted table material prevents the checker from producing a conclusion.

Mitigation: Provide the AP aging and payment-plan table with recognizable headers and source rows; treat missing-material output as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ap-aging-plan-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable terminal text or JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source lines when checks run; insufficient input returns missing-material guidance instead of a clean result.]

## Skill Version(s):

1.0.59 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
