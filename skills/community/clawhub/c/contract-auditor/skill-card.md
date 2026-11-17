## Description:

Contract Auditor reviews Chinese Word contracts for payment, delivery, compliance, and risk issues, then produces audit findings, recommendations, and annotated contract outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjmfjoy](https://clawhub.ai/user/bjmfjoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and contract-review teams use this skill to screen Chinese Word contracts for common clause issues, summarize risk levels, and generate Markdown or Word-based annotations for manual follow-up. Its findings should be treated as drafting support rather than legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contracts may contain confidential or sensitive commercial information.

Mitigation: Process contracts only in an environment approved for the document sensitivity, and avoid uploading or sharing generated reports outside the intended review workflow.

Risk: The audit output may be incomplete or legally incorrect.

Mitigation: Use findings as drafting support and require manual review by qualified legal or contract staff before relying on changes.

Risk: Annotated Word output can overwrite or confuse the original contract record if paths are reused.

Mitigation: Write annotations to a separate output filename and retain an unchanged copy of the source contract.

Risk: Unpinned document-processing dependencies can change behavior over time.

Mitigation: Pin and test python-docx before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bjmfjoy/skills/contract-auditor)
- [Skill overview](SKILL.md)
- [Design document](docs/DESIGN.md)
- [Requirements](requirements.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown audit reports, annotated Markdown text, and annotated Word document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include risk levels, issue counts, clause locations, descriptions, and suggested revisions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
