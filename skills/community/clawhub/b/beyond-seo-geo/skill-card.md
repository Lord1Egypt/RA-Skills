## Description: <br>
Use for SEO audits, AEO/GEO strategy, local SEO, backlink review, competitor research, keyword mapping, Apify/native scraping workflows, and client-ready SEO reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyondtahir](https://clawhub.ai/user/beyondtahir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketers, agencies, and developers use this agent skill to run evidence-based SEO, local SEO, backlink, competitor, and AEO/GEO workflows. It helps produce prioritized audits, growth plans, keyword maps, reports, templates, code, configuration guidance, and safe scraping or export-based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require sensitive credentials such as an Apify token or SEO/business exports. <br>
Mitigation: Use environment variables or a secret manager, prefer scoped or read-only credentials, avoid writing tokens into skill files, reports, templates, manifests, or logs, and do not repeat pasted tokens in final answers. <br>
Risk: Scraping, crawling, and scheduled monitoring can collect private, login-only, or excessive data if used without clear scope and authorization. <br>
Mitigation: Use authorized public or exported data, sanitize business exports, keep crawls and SERP samples credit-safe by default, and review scheduled Apify monitoring before enabling it. <br>
Risk: SEO, backlink, and AEO/GEO recommendations can mislead users if rankings, traffic, backlink counts, search volume, or AI citations are invented or overpromised. <br>
Mitigation: Follow the skill's evidence-first workflow, label estimates clearly, treat community actor outputs as directional unless verified, and avoid ranking, traffic, backlink, or AI-citation guarantees. <br>
Risk: Backlink workflows could be misused for spam, unsafe paid links, or over-optimized anchors. <br>
Mitigation: Use backlink sources as seed assets and posting-pattern examples, prioritize relevance and authority, avoid bulk link packages and spam outreach, and review paid-link risk before recommending action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beyondtahir/beyond-seo-geo) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/beyondtahir) <br>
- [Google Search Central: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) <br>
- [Google Search Central: Google Search generative AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) <br>
- [Google Search Central: Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) <br>
- [Bing Webmaster Tools: AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c) <br>
- [Perplexity Hub](https://www.perplexity.ai/hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, structured tables, CSV templates, JSON-adjacent reports, Python helper scripts, and shell/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should label missing or estimated SEO data, avoid ranking guarantees, and separate confirmed evidence from recommended checks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact files also reference 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
