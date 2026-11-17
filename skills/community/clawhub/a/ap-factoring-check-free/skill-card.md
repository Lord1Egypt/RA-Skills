## Description:

Locally checks accounts-payable factoring and discounting tables for row-level recalculations, total-row consistency, duplicate supplier/document rows, blank fields, and negative amounts, with source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounts-payable staff use this skill during month-end close, reconciliation, or inventory-count checkpoints to check an accounts-payable factoring and discounting table before relying on it. It performs deterministic table checks and reports missing inputs instead of making conclusions from incomplete material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free checker as a complete audit even though some checks are explicitly not included and contract, rate, bank-record, and paid-version checks are out of scope.

Mitigation: Review the listed free-version limitations and validate contract terms, rates, bank records, and omitted checks through separate finance controls before close or audit use.

Risk: Incomplete or malformed input can prevent execution or make the result unsuitable for decision-making.

Mitigation: Provide a complete accounts-payable factoring table with the required headers and review any insufficient-input messages before rerunning the check.

Risk: The output is deterministic table analysis, not a judgment about financing fairness, accounting treatment, or external source-of-truth records.

Mitigation: Have qualified finance staff reconcile findings against ERP exports, agreements, bank records, and organization-specific accounting policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ap-factoring-check-free)

## Skill Output:

**Output Type(s):** [text, json, analysis, shell commands]

**Output Format:** [Human-readable text or JSON produced by a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite row-level source context; insufficient input returns missing requirements and no conclusion.]

## Skill Version(s):

1.0.60 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
