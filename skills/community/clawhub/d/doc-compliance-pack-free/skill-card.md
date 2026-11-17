## Description:

A local checker for invoices and supporting documents that runs 14 built-in document compliance checks per material directory and prints one conclusion line per material, with findings citing the source file and line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement, accounts payable, finance, accounting, internal-control, and bookkeeping users can run the skill before signing or paying to check submitted invoice, contract, bid, reimbursement, export-rebate, purchase, and trade-document materials. The skill is intended as a local precheck that highlights arithmetic, consistency, and wording issues with source-file and line references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a clean result as approval to sign, pay, file taxes, or publish regulated content.

Mitigation: Use the output as a local precheck only, review the cited source materials, and obtain legal, tax, audit, or business approval where required.

Risk: Incomplete or incorrectly structured materials can leave checks unexecuted rather than passed.

Mitigation: Place each material set in its own directory, include recognizable headers, and review the checks_not_run and sub_checks_not_run sections before relying on the findings.

Risk: The free release omits cross-material dashboards, risk-ranked sign-or-pay action lists, grouped common issues, and Markdown or CSV report export.

Mitigation: Treat those omitted items as not performed and do not infer cross-material approval or exported reporting from this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/doc-compliance-pack-free)
- [Artifact skill documentation](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON emitted to stdout, including per-material conclusions and source-file line references for findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally without network access, persistence, credential use, or file writes according to security evidence; insufficient inputs produce no compliance conclusion.]

## Skill Version(s):

1.0.30 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
