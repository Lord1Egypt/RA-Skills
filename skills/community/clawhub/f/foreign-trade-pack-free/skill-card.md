## Description:

A local checker for foreign trade and export worksheets that runs 14 built-in checks per object directory and reports one conclusion line per object with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as foreign-trade accountants, documentation staff, customs declaration teams, and export tax rebate reviewers use this skill to check exported worksheet materials at recurring declaration, collection, rebate, import clearance, freight, and insurance settlement points. It helps review submitted text materials locally and surfaces findings with source line references, but it does not replace customs, tax, banking, audit, or legal approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a clean local check as tax, customs, banking, audit, or legal approval.

Mitigation: Present results as review support only and require qualified review before relying on them for filings, settlements, audits, or legal decisions.

Risk: The free release does not run every possible export review, and some checks or sub-checks may be listed as not run.

Mitigation: Review the reported checks_not_run and sub_checks_not_run before relying on a result, especially when a clean result is produced from partial materials.

Risk: Incomplete or poorly structured materials can leave checks unexecuted rather than validated.

Mitigation: Provide one directory per checked object and include clearly segmented source worksheets so unexecuted checks are visible and can be corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/foreign-trade-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Shell commands]

**Output Format:** [Plain text or JSON printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite the checked object, check name, source file, and source line when available; insufficient input exits without producing a pass/fail conclusion.]

## Skill Version(s):

1.0.24 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
