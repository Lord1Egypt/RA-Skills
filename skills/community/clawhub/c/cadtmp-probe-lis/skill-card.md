## Description:

Analyzes local DWG, DXF, DWT, and PDF drawings to produce evidence-linked geometry, semantic, and discipline-specific recognition candidates without calculating final quantities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use the skill to inspect local CAD and PDF drawings, extract geometry and discipline-specific recognition or measurement candidates, and review each candidate against its source evidence. It does not calculate final project quantities or costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic converter discovery may run untrusted code from a shared temporary folder.

Mitigation: Prefer DXF inputs or use a verified converter from PATH; avoid relying on converters discovered in shared temporary folders.

Risk: Project evidence may be stored locally, and first-run setup may download packages.

Mitigation: Review generated or stored evidence before sharing, and run scrubber --apply only on disposable copies.

## Reference(s):

- [CAD Tmp Probe release page](https://clawhub.ai/lisong2003-lgtm/skills/cadtmp-probe-lis)
- [QTO linkage documentation](docs/qto-linkage.md)
- [Regression and scrubbing checklist](docs/regression-scrub-checklist.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON candidate records with geometry, semantics, measurements, and source-evidence references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recognition and measurement candidates only; no final quantities, material totals, costs, or settlement quantities.]

## Skill Version(s):

0.0.2 (source: server-resolved release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
