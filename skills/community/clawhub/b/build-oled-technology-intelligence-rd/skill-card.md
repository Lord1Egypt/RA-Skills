## Description:

Builds a source-traceable, multi-page technology-intelligence HTML portal for OLED or another defined technology domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, R&D analysts, strategy teams, competitive-intelligence teams, and IP teams use this skill to turn reviewed company, technology-route, event, publication, and patent records into a refreshable local intelligence portal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer writes local portal pages into a user-selected output directory, and --overwrite can replace generated page names there.

Mitigation: Use a new empty output directory, avoid symlinked paths, and enable --overwrite only after confirming the directory contents.

Risk: Technology, company, event, publication, and patent summaries can mislead readers if based on unreviewed records, ambiguous entity matches, or unsupported rankings.

Mitigation: Require reviewed evidence IDs, explicit methodology and limitations, deduplicated records, disclosed patent count units, and clear separation of source facts from analyst inference.

## Reference(s):

- [Organization Mapping and OLED Seed Universe](references/company-mapping.md)
- [Technology Taxonomy and OLED Seed Tags](references/tech-tags.md)
- [Portal Data Processing and Validation](references/data-processing.md)
- [Portal HTML Structure and Scientific Editorial Design](references/html-templates.md)
- [PatSnap Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and validated JSON input contracts; the renderer produces self-contained HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated portals are local static HTML pages built from reviewed UTF-8 JSON input and are designed to avoid runtime network dependencies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
