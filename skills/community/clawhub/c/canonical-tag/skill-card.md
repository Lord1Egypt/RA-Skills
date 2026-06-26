## Description: <br>
Guides canonical URL configuration to consolidate duplicate content and declare preferred URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kostja94](https://clawhub.ai/user/kostja94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO practitioners use this skill to choose canonical URLs, configure canonical tags, and align redirects, hreflang, sitemap, and indexing signals for duplicate URL variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project context files may contain sensitive site details if the agent reads them before giving canonical URL guidance. <br>
Mitigation: Review `.claude/project-context.md` and `.cursor/project-context.md` before use and keep secrets or private operational details out of those files. <br>
Risk: Redirect and canonical configuration changes can affect routing, indexing, and search visibility if applied incorrectly. <br>
Mitigation: Review generated changes deliberately, test redirects and canonical tags before deployment, and validate canonical URLs with search tooling after release. <br>


## Reference(s): <br>
- [ClawHub canonical-tag release page](https://clawhub.ai/kostja94/canonical-tag) <br>
- [Google Search Central: Consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) <br>
- [Google Search Central: HTTPS as a ranking signal](https://developers.google.com/search/blog/2014/08/https-as-ranking-signal) <br>
- [Alignify URL optimization](https://alignify.co/zh/seo/url-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include canonical URL recommendations, HTML tags, framework metadata examples, and redirect configuration snippets.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
