## Description:

Create an auditable technology-intelligence briefing for named companies and/or a technical topic using patent, scientific-literature, and current-news evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and IP researchers use this skill to scope and generate evidence-backed technology intelligence briefings for companies, technical topics, patent-and-literature scans, subtechnology maps, and technical trend reports. The skill supports research and decision preparation, but the artifact states it is not legal advice, investment advice, or a completeness guarantee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that the HTML renderer executes a local Python data file, which is a high-impact under-disclosed code-execution risk.

Mitigation: Install only if comfortable running the local Python renderer; create v2_data.py through a trusted workflow, review it as code, and avoid using data files supplied by untrusted sources.

Risk: Technology intelligence briefings may be mistaken for legal advice, investment advice, or a completeness guarantee.

Mitigation: Use the briefing as research support only and verify material decisions against cited primary sources and current authoritative records.

Risk: Findings can become misleading if patent populations, displayed samples, legal entities, source availability, or counting units are conflated.

Mitigation: Record the scope, connector/tool provenance, date field, counting unit, family and deduplication rule, section status, and limitations; keep population counts separate from selected displayed records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/create-technology-intelligence-briefing-ip)
- [Request parsing rules](references/parse_rules.md)
- [Technology keyword expansion](references/keyword_expansion.md)
- [Company aliases](references/company_aliases.json)
- [Technology intelligence briefing trace template](references/trace_template.md)
- [Renderer data contract](scripts/v2_data.sample.py)
- [Advanced Patent Search marketplace](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [Patent Briefing marketplace](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)
- [Deep Patent Mining marketplace](https://open.patsnap.com/marketplace/mcp-servers/patent-mining)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Static HTML briefing plus Markdown trace, with Python data-contract files and shell commands when report generation is executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are evidence-backed research support artifacts with explicit scope, source, count, limitation, and reproducibility notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
