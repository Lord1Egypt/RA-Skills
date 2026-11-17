## Description:

Helps agents plan website page hierarchy, navigation, URL structure, visual sitemaps, and internal linking for new or restructured sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, designers, and site owners use this skill to organize website pages, navigation, URLs, visual sitemap diagrams, and internal links before building or restructuring a site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local product-marketing context files if present.

Mitigation: Review those context files before use and avoid placing sensitive credentials or restricted information there unless the agent environment is approved for that data.

Risk: The skill can plan page hierarchy, navigation, URLs, and visual sitemaps, but it is not a technical SEO or structured-data implementation tool.

Mitigation: Use a dedicated SEO audit or schema markup workflow for XML sitemaps, crawl errors, and schema implementation before making production changes.

## Reference(s):

- [Site Type Templates](references/site-type-templates.md)
- [Navigation Patterns](references/navigation-patterns.md)
- [Mermaid Diagram Templates](references/mermaid-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with ASCII trees, Mermaid diagrams, tables, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local product marketing context files when present before asking follow-up questions.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
