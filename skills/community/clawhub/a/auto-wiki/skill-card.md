## Description:

Knowledge compiler that teaches agents to incrementally compile source files into persistent local wikis for cross-session knowledge accumulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanlinlibham](https://clawhub.ai/user/hanlinlibham)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to let an agent build and maintain a local topic wiki from supplied source materials, then recall, query, lint, or fill gaps in accumulated knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently modifies a local .wiki knowledge base.

Mitigation: Confirm the wiki location before first creation and review proposed ingest, lint, and deep-dive writes before allowing changes.

Risk: Generated _report.html output can run remote browser JavaScript over private wiki content.

Mitigation: Avoid generating or opening reports for sensitive wikis until report output is sanitized and the remote dependency is removed or pinned with integrity controls.

Risk: Optional network features and external validators can expose project context to approved destinations.

Mitigation: Keep WebSearch, domain MCP, and external validator use disabled for confidential projects unless the destination and data being sent are explicitly approved.

## Reference(s):

- [Auto Wiki ClawHub Skill Page](https://clawhub.ai/hanlinlibham/skills/auto-wiki)
- [Ingest Protocol](references/ingest-protocol.md)
- [Query Protocol](references/query-protocol.md)
- [Lint Protocol](references/lint-protocol.md)
- [Storage Specification](references/storage-spec.md)
- [Information Source Validation](references/source-validation.md)
- [Wiki Page Format](references/wiki-format.md)
- [FIBO Pensions Seed Vocabulary](seeds/fibo-pensions.md)
- [FIBO Specification](https://spec.edmcouncil.org/fibo/)
- [FIBO MCP Runtime Logic Validator](validators/fibo-mcp.md)
- [NeuroFusionAI/fibo-mcp](https://github.com/NeuroFusionAI/fibo-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional shell commands and local wiki file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .wiki/{topic}/ Markdown pages, SQLite data, and generated reports after user confirmation.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
