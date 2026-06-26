## Description: <br>
Anti-SEO deep consumer research tool that helps users make purchase decisions by adapting searches, credibility scoring, and reports to the user's language and region. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmosHc](https://clawhub.ai/user/AmosHc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research consumer purchases across regional search engines, e-commerce review sources, social comments, forums, and safety-event sources. It filters suspected advertising or astroturfing, scores candidate products, resolves conflicting evidence, and produces recommendation reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs included Python scripts, performs web searches, fetches third-party pages, writes reports, and may keep a local cache under the scripts directory. <br>
Mitigation: Install only when this behavior is acceptable, supervise proposed commands before execution, avoid highly sensitive research queries, and clear the local cache after sensitive work. <br>
Risk: Consumer research can include misleading, sponsored, outdated, or low-quality web content despite filtering and scoring. <br>
Mitigation: Review source links, quotes, safety findings, and data-transparency sections before relying on recommendations for purchasing decisions. <br>


## Reference(s): <br>
- [Anti-SEO Researcher on ClawHub](https://clawhub.ai/AmosHc/anti-seo-researcher) <br>
- [Anti-SEO Deep Consumer Researcher - Detailed Reference Manual](references/SKILL_REFERENCE.md) <br>
- [Credibility Scoring Rules](references/credibility_rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with JSON task/category configuration and scored JSON intermediate outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated in the user's language; scripts may write local report, scoring, search-result, and cache files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
