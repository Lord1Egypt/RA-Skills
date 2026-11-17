## Description:

Scans plain-text contracts offline for common high-risk clause patterns, infers contract type, and produces risk-ranked findings, missing-clause checks, and questions to ask before signing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Consumers, renters, employees, freelancers, and reviewing agents use this skill for first-pass triage of plain-text contracts before signing or requesting legal review. It helps surface common red flags, missing protections, and concrete negotiation questions, but it is not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pattern-based contract triage can miss issues or overstate a clause's effect.

Mitigation: Treat results as screening guidance, preserve the quoted contract language as evidence, and consult a licensed attorney for high-value contracts or serious findings.

Risk: Incomplete text extraction or OCR errors can create false negatives.

Mitigation: Check that all pages, schedules, exhibits, and fee tables are present and readable before scanning.

Risk: Short or unusual documents may be assigned the wrong contract type.

Mitigation: Review the inferred type and rerun with an explicit contract type when the classification looks wrong.

Risk: Contract text can contain sensitive personal, employment, or financial information.

Mitigation: Use the offline local scanner path described by the artifact and avoid sending sensitive contracts to unrelated network services.

## Reference(s):

- [Clause Guide](artifact/references/clause-guide.md)
- [Sample Lease](artifact/references/sample-lease.txt)
- [ClawHub Release Page](https://clawhub.ai/voronindenis5/skills/contract-red-flag-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain-text or JSON contract-risk report with matched excerpts, ranked findings, missing-clause checklist, scrutiny score, and question list.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs offline with Python stdlib; exit code 2 indicates HIGH findings are present.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
