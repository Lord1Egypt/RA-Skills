## Description:

Create or update a traceable, self-contained HTML patent intelligence report for a life-sciences technology, target, drug, antibody, ADC, company, or patent set, including claims, sequences or conjugate technology, experiments, pipeline and clinical context, scientific evidence, deals or news, and inline patent-figure evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to create or refresh evidence-traceable life-sciences patent landscape and deep-dive reports. It is intended for patent intelligence reporting with clinical, scientific, commercial, and figure evidence kept distinct from legal or clinical conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential sequences, patent files, figures, or business context may be routed to selected PatSnap MCPs or other permitted external services during report creation.

Mitigation: Confirm data-sharing authorization and permitted services before installation or use.

Risk: Generated patent intelligence may contain source, citation, or interpretation errors and is not a legal opinion or clinical validation.

Mitigation: Review source accuracy, legal-status caveats, and evidence boundaries before relying on the report.

Risk: Invented or mismatched links, missing local figure assets, or unsupported frontend routes could weaken traceability.

Mitigation: Run the skill's HTML, link, source-map, local-asset, responsive, and print validation checks before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-life-sciences-patent-report-ls)
- [Life Sciences Patent Report Specification](references/report-spec.md)
- [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [PatSnap Target Disease MCP](https://open.patsnap.com/marketplace/mcp-servers/target-disease)
- [PatSnap Drug Asset MCP](https://open.patsnap.com/marketplace/mcp-servers/drug-asset)
- [PatSnap Clinical Trials MCP](https://open.patsnap.com/marketplace/mcp-servers/clinical-trials)
- [PatSnap Scientific Translational Evidence MCP](https://open.patsnap.com/marketplace/mcp-servers/scientific-translational-evidence)
- [PatSnap Regulatory Guidelines MCP](https://open.patsnap.com/marketplace/mcp-servers/regulatory-guidelines)
- [PatSnap Current Awareness MCP](https://open.patsnap.com/marketplace/mcp-servers/current-awareness)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Self-contained HTML report with source records, audit tables, validation notes, and optional local figure links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source identifiers, exact URLs, retrieval context, confidence notes, and limitations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
