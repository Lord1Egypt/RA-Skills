## Description: <br>
Audits URLs for AI citation eligibility, AI Overview and citation worthiness, llms.txt readiness, entity coverage, and SEO regressions without requiring API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[automatelab](https://clawhub.ai/user/automatelab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SEO practitioners, and content teams use this skill to audit public pages for blockers that prevent AI systems from citing or summarizing them. It can generate prioritized fixes, llms.txt content, AEO/GEO rewrite drafts, entity checks, and SEO regression comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates runtime behavior to an npm package installed through npx. <br>
Mitigation: Review the npm package before installing or enabling it in an MCP host. <br>
Risk: URL audits may access sites outside the user's control. <br>
Mitigation: Use the skill only for sites the user is allowed to audit. <br>
Risk: Generated SEO fixes or rewrites may be incomplete or misleading if applied without review. <br>
Mitigation: Have a knowledgeable reviewer check reports, generated llms.txt content, and AEO/GEO rewrites before publishing changes. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/AutomateLab-tech/ai-seo-mcp) <br>
- [ClawHub release page](https://clawhub.ai/automatelab/automatelab-ai-seo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reports with configuration snippets, generated llms.txt content, rewrite drafts, and prioritized fix guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys required; analysis is based on read-only HTTP checks against target URLs.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
