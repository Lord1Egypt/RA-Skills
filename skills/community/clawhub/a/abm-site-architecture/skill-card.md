## Description: <br>
Helps agents plan, map, or restructure website page hierarchy, navigation, URL structure, visual sitemaps, and internal linking while distinguishing site architecture work from technical SEO tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, website strategists, marketers, designers, and developers use this skill to turn business context and content inventory into page hierarchies, URL maps, navigation specs, visual sitemap diagrams, and internal linking plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read a local product marketing context file when available, which could expose sensitive or stale marketing strategy to the agent workflow. <br>
Mitigation: Review `.agents/product-marketing-context.md` or `.claude/product-marketing-context.md` before use and remove secrets, confidential strategy, or outdated positioning. <br>
Risk: Site architecture recommendations can affect navigation, URL changes, redirects, and internal linking, so incorrect guidance may create findability or SEO regressions. <br>
Mitigation: Have stakeholders review the proposed hierarchy, URL map, and redirect plan before implementation, especially for existing sites. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/mariokarras/abm-site-architecture) <br>
- [Mermaid Diagram Templates](references/mermaid-templates.md) <br>
- [Navigation Patterns](references/navigation-patterns.md) <br>
- [Site Type Templates](references/site-type-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown with ASCII trees, Mermaid diagrams, URL map tables, navigation specifications, and internal linking plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommended page hierarchy, URL patterns, header and footer navigation, breadcrumb guidance, redirects to preserve moved URLs, and cross-section linking opportunities.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
