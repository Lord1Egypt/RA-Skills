## Description: <br>
Knowledge compiler: teaches agents to incrementally compile source files into persistent wikis for cross-session knowledge accumulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanlinlibham](https://clawhub.ai/user/hanlinlibham) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use auto-wiki to compile supplied source material into a persistent local `.wiki/` knowledge base, then recall, query, lint, and optionally fill gaps in that accumulated wiki. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local wiki writes can create or modify Markdown pages, SQLite data, and Obsidian configuration under `.wiki/`. <br>
Mitigation: Confirm the target wiki location before first creation, keep `.wiki/` out of project commits unless intentionally versioned, and review created or updated pages after ingest. <br>
Risk: Lint repairs and deep-dive ingestion can introduce incorrect or outdated knowledge into the persistent wiki. <br>
Mitigation: Review lint repairs and gap-fill sources before accepting them, require confirmation for deep-dive gap filling, and label contested or unverified claims. <br>
Risk: Optional WebSearch, WebFetch, domain data MCPs, and external validators may expose sensitive topics or source material outside the local environment. <br>
Mitigation: Use passive file-based mode for sensitive domains and avoid optional external validators or search tools unless that disclosure is acceptable. <br>
Risk: Generated `_report.html` loads third-party JavaScript from a CDN. <br>
Mitigation: Open reports only in trusted contexts or avoid report generation when third-party CDN loading is not acceptable. <br>


## Reference(s): <br>
- [auto-wiki ClawHub release](https://clawhub.ai/hanlinlibham/auto-wiki) <br>
- [Storage Specification](references/storage-spec.md) <br>
- [Wiki Page Format](references/wiki-format.md) <br>
- [Ingest Protocol](references/ingest-protocol.md) <br>
- [Query Protocol](references/query-protocol.md) <br>
- [Lint Protocol](references/lint-protocol.md) <br>
- [Information Source Validation](references/source-validation.md) <br>
- [FIBO MCP Validator](validators/fibo-mcp.md) <br>
- [Financial Industry Business Ontology](https://spec.edmcouncil.org/fibo/) <br>
- [NeuroFusionAI fibo-mcp](https://github.com/NeuroFusionAI/fibo-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown wiki pages, SQLite-backed local data files, shell command snippets, configuration updates, and health or gap reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local `.wiki/` content; optional active search and external validation depend on the user's configured tools.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
