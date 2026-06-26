## Description: <br>
Guides an agent through structured SEO audits, technical SEO diagnostics, on-page review, content quality assessment, and prioritized recommendations for improving organic search performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and site operators use this skill to diagnose crawlability, indexation, Core Web Vitals, on-page SEO, content quality, and site-type-specific SEO issues. It produces an audit report with evidence, impact, fixes, and a prioritized action plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local product marketing context before an audit, which could include sensitive business or positioning details. <br>
Mitigation: Review local marketing context files before use and remove sensitive material that should not be included in the SEO analysis. <br>
Risk: SEO crawling, rendering, or analytics tools may send URLs, page content, or site context to external services. <br>
Mitigation: Use trusted Firecrawl and SEO tooling, and only submit URLs or analytics context that is approved for analysis. <br>
Risk: The audit can produce incorrect or misleading SEO recommendations if the available evidence is incomplete or tool results are stale. <br>
Mitigation: Review recommendations against current site data, Search Console or analytics evidence, and implementation constraints before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mariokarras/abm-seo-audit) <br>
- [Publisher Profile](https://clawhub.ai/user/mariokarras) <br>
- [AI Writing Detection](references/ai-writing-detection.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown audit report with checklists, findings, recommendations, and inline shell commands where tool usage is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are organized by issue, impact, evidence, fix, and priority.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
