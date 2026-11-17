## Description:

Converts prepared, screened, and tagged patent datasets into evidence-bounded competitive technology insight reports in Markdown or self-contained HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IP analysts, strategy teams, and agents use this skill to turn validated tagged patent records into management-grade competitive technology reports, including technology-route matrices, competitor profiles, trend signals, and bounded R&D/IP actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent trend reports can become misleading if the input dataset is unscreened, untagged, incomplete, or mixed across inconsistent counting units.

Mitigation: Use the skill's field-readiness gate, disclose provenance, coverage, counting unit, missingness, and tag semantics, and omit unsupported deep-analysis sections.

Risk: Connector use can expose API keys or private connection URLs if setup details are copied into reports.

Mitigation: Use PatSnap MCP services only when retrieval or validation is needed, inspect live schemas before use, and keep API keys and private connection URLs out of generated artifacts.

Risk: Patent counts or tags may be overread as proof of quality, enforceability, market success, manufacturing capability, freedom to operate, or health/product efficacy.

Mitigation: Keep patent observations separate from domain mapping and analyst interpretation, use bounded language, and require claims, legal-status, technical, regulatory, and market validation before strategic decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/analyze-technology-patent-trends-ip)
- [White-paper framework](artifact/references/white-paper-framework.md)
- [HTML report template specification](artifact/references/html-report-template-spec.md)
- [PatSnap Developer Center](https://open.patsnap.com/devportal)
- [Advanced Patent Search MCP service](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing MCP service](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Deep Patent Mining MCP service](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or self-contained HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires prepared, screened, and tagged patent data; HTML outputs must be self-contained, accessible, and free of external runtime dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
