## Description:

A free local checker for monthly fire-facility inspection and maintenance records that runs six table-consistency checks, cites source lines for findings, and gives no conclusion when evidence is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External fire-safety administrators and responsible staff at property, factory, mall, and school sites use this skill to check monthly inspection and maintenance record tables before archiving, monthly summaries, or supervisory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake record-table consistency checks for legal, technical, or on-site fire-safety certification.

Mitigation: Treat results as record-review support only; use qualified inspections, technical review, and applicable legal processes for compliance decisions.

Risk: The free version omits several checks, including fault-closure timing, unclosed fault lists, maintenance-cycle checks, qualification coverage, and remediation summaries.

Mitigation: Review the omitted checks before relying on the output, and do not treat an absence of findings as proof that the records are complete or compliant.

Risk: Inspection and maintenance records may contain sensitive facility information.

Mitigation: Run the local Node.js checker only in a trusted environment and keep source materials within approved handling procedures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/fire-safety-inspection-check-free)
- [SKILL.md](artifact/SKILL.md)
- [Local runner](artifact/scripts/run.mjs)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text or JSON report with cited source lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against a single text input containing the record table; insufficient input returns missing-field guidance instead of a compliance conclusion.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
