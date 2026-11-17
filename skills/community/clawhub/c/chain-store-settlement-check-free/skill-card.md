## Description:

A local settlement-table checker for chain franchise stores that recalculates rows, checks totals, detects duplicates and blanks, and cites the source line for each finding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashier teams use this skill during monthly chain-store settlement review to recalculate settlement rows, verify totals, and identify duplicate or incomplete entries before payment decisions. It is a deterministic checker for provided settlement-table text, not legal, tax, contract, or full audit advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes copied settlement-table data that may contain sensitive business financial information.

Mitigation: Run it only in environments approved for that data and review the local output before sharing results.

Risk: The free release performs only its listed checks and may omit issues covered by contract, tax, legal, or full audit review.

Mitigation: Use the output as a settlement-table arithmetic and completeness aid, and route contract, tax, legal, and audit questions to the appropriate review process.

Risk: Insufficient or malformed input can prevent the checker from reaching a conclusion.

Mitigation: Provide settlement-table text with headers and required columns, and treat insufficient-input responses as no conclusion rather than as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/chain-store-settlement-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable text or JSON containing executed checks, findings, cited source lines, omitted checks, and insufficiency guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with bundled Node.js code; does not require registration, an API key, or network access according to release evidence.]

## Skill Version(s):

1.0.53 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
