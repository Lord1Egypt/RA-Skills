## Description:

A free deterministic checker for accounts-payable provisional ledgers, covering provision amount recalculation, reversal checks, invoice-versus-provisional differences, balance roll-forward, column totals, duplicate document numbers, blanks, negatives, and source-line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance staff and accounts-payable accountants use this skill before monthly close to check AP provisional ledger rows, totals, missing values, duplicate document numbers, and basic invoice/provisional differences. It is designed to report cited findings from the provided ledger text, and to withhold conclusions when required input is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on the free version for accounting checks that it explicitly does not perform.

Mitigation: Review the free-version limitations before relying on the output; omitted checks include higher-level invoice, adjustment, duplicate-contract, AP-detail, and long-aged provisional balance judgments.

Risk: The skill processes AP ledger text, which may contain sensitive commercial or financial information.

Mitigation: Run it only in an environment where local handling of the ledger text is acceptable; server security evidence describes the skill as local, read-only, and without hidden network behavior.

Risk: The skill does not provide accounting, audit, tax, invoice-validity, or business-judgment opinions.

Mitigation: Treat its findings as deterministic ledger checks and have responsible finance or audit personnel review material conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/ap-provisional-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or JSON check results with source line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local Node.js checks; insufficient input returns missing fields instead of conclusions.]

## Skill Version(s):

1.0.66 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
