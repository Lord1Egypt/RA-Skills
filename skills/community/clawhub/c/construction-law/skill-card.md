## Description:

A construction-law toolkit for analyzing FIDIC, PSSCOC, SIA, NEC notice workflows, and Singapore SOP Act matters, with tools for notices, claims, EOT applications, obligations registers, and deadline calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redkiwi1688-prog](https://clawhub.ai/user/redkiwi1688-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External construction lawyers, in-house counsel, contract managers, quantity surveyors, claims consultants, and project managers use this skill to structure contract analysis, claim preparation, notice tracking, obligations registers, and Singapore SOP Act deadline workflows.

### Deployment Geography for Use:

Global, with Singapore-specific SOP Act and bundled Singapore holiday data coverage.

## Known Risks and Mitigations:

Risk: Matter files and generated reports may contain confidential legal or commercial information.

Mitigation: Keep all matter inputs and generated outputs in approved confidential storage.

Risk: CSV or spreadsheet outputs may be opened in tools that transform or execute spreadsheet content.

Mitigation: Review CSV outputs before opening or sharing them in spreadsheet applications.

Risk: Optional BCA mirror or scheduled refresh workflows add background maintenance and data-handling obligations.

Mitigation: Enable those workflows only when explicitly needed and governed by local operational controls.

Risk: Construction-law drafting and deadline outputs can be incorrect if applied without checking contract amendments, governing law, holiday coverage, and current regulatory updates.

Mitigation: Review generated analysis against the actual contract, authoritative legal sources, and qualified professional judgment before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redkiwi1688-prog/skills/construction-law)
- [FIDIC reference](artifact/references/fidic.md)
- [Singapore construction law reference](artifact/references/singapore.md)
- [Claims reference](artifact/references/claims.md)
- [Disputes reference](artifact/references/disputes.md)
- [Procurement reference](artifact/references/procurement.md)
- [Legal systems reference](artifact/references/legal_systems.md)
- [Holiday file format](artifact/docs/holiday-file-format.md)
- [BCA circulars](https://www1.bca.gov.sg/resources/circulars/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, plain text, CSV, Excel workbooks, Word documents, JSON configuration, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are local workflow aids and should be reviewed before legal or commercial reliance.]

## Skill Version(s):

2.11.5 (source: evidence.release.version, CHANGELOG.md, scripts/version.py; pyproject.toml reports 2.11.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
