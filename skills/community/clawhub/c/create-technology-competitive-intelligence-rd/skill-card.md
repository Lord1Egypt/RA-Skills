## Description:

Create an evidence-led technology competitive-intelligence report for a defined company, technology, market, and review period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Global R&D, strategy, product, and IP teams use this skill to build reviewed competitive-intelligence briefings for a defined focal organization, technology scope, market, geography, and time window. It supports competitor tiering, patent and technology comparisons, customer or partner mapping, event monitoring, threat assessment, and actionable R&D recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Competitive-intelligence inputs may contain sensitive company, product, market, or IP information.

Mitigation: Use authorized reviewed data, retain source identifiers, and avoid including credentials or private data in generated reports.

Risk: Patent and market evidence could be misread as legal, valuation, investment, or commercial advice.

Mitigation: Keep limitations visible, label assumptions and analyst inference, and recommend qualified patent counsel for claim-level infringement, validity, or FTO analysis.

Risk: Optional connector output can be incomplete or unavailable.

Mitigation: Require analyst review of connector results, preserve returned record links or identifiers, and document limitations when connectors are unavailable.

Risk: The renderer writes an HTML file to the requested output path and creates parent directories.

Mitigation: Choose the output path deliberately and review generated files before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-technology-competitive-intelligence-rd)
- [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [template_v12.html](references/template_v12.html)
- [template_v11.html](references/template_v11.html)
- [template_v8.html](references/template_v8.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON data preparation, shell commands, and generated self-contained HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses reviewed input data and explicit template tokens; V12 is the default report template, with V11 and V8 available when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
