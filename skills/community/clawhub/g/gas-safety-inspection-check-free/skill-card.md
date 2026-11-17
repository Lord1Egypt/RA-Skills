## Description:

燃气设施月度巡检与隐患整改记录逐行核对，免费版执行 6 项检查（检查频次覆盖、软管/管件有效期、报警器年检复算、重复登记、合计行逐列复核、字段与取值合法性），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External safety administrators, store managers, property teams, factory operators, and school cafeteria managers use this skill to check monthly gas facility inspection and hazard-rectification records for missing inspections, overdue hose or pipe components, alarm inspection date issues, duplicate entries, total-row mismatches, and invalid field values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake record-consistency findings for proof that a gas facility is safe, compliant, or fully remediated.

Mitigation: Use the output as a record-checking aid only, and require qualified safety review, inspection evidence, and regulatory judgment before operational or compliance decisions.

Risk: The free release omits several checks, including full hazard-rectification closure, supplier qualification coverage, contract coverage, and physical safety determinations.

Mitigation: Review the disclosed omitted and out-of-scope checks, then supplement with manual review, source documentation, or a fuller inspection process where those checks matter.

Risk: Incomplete or malformed inspection records can produce missing-input responses or limited findings.

Mitigation: Provide records with the required table headers and inspect missing-field guidance before relying on any findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/gas-safety-inspection-check-free)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON findings with cited source rows and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs over user-provided inspection-record text or JSON input; insufficient material returns missing-field guidance instead of a safety conclusion.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
