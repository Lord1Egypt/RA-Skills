## Description:

This Chinese-language skill locally checks clinic billing and medical insurance settlement tables for row arithmetic, totals, duplicates, blanks, and negative amounts, with findings tied to source rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Clinic finance and cashier staff use this skill during monthly closing or reconciliation to check medical billing and insurance settlement tables for arithmetic consistency, duplicate settlement batches, missing required fields, and negative amounts. It helps reviewers find table-level issues but does not determine local insurance policy correctness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake table arithmetic checks for validation of local medical insurance policy rules.

Mitigation: Review findings against the original records, local insurance rules, and settlement agreements before acting on them.

Risk: The free version does not run every check listed for the related full version.

Mitigation: Review the reported checks_not_run or withheld-check list before relying on the result as complete coverage.

Risk: Incomplete or malformed input can prevent the skill from issuing a conclusion.

Mitigation: Provide the settlement table with required headers and source rows, and treat insufficient-input output as a request for more material rather than a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/clinic-revenue-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Chinese-language CLI text or pretty-printed JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution; accepts JSON or pasted tabular text; security evidence reports no network use, persistence, credential handling, or hidden behavior.]

## Skill Version(s):

1.0.45 (source: server release metadata; artifact frontmatter says 1.0.46)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
