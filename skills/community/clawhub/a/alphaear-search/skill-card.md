## Description: <br>
Perform finance web searches and local context searches for general finance information from Jina, DuckDuckGo, Baidu, or a local document store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve finance-related web results, aggregate multiple search engines, reuse recent cached results when appropriate, and query a local finance news database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance queries, selected URLs, extracted page text, and sentiment inputs may be cached locally or sent to Jina and configured model providers. <br>
Mitigation: Use the skill only with data suitable for those services, manage or isolate the local SQLite cache, and disable enrichment or sentiment paths for sensitive client, compliance, trading, or proprietary research. <br>
Risk: The security scan found non-malicious but suspicious behavior beyond the short description, including external page extraction, provider-based analysis, model downloads, and persistent caching. <br>
Mitigation: Review the artifact and runtime configuration before installation, keep required API keys scoped, and run it in an environment where outbound requests and stored cache contents are acceptable. <br>


## Reference(s): <br>
- [AlphaEar Search ClawHub page](https://clawhub.ai/zhouzhonglu8-png/alphaear-search) <br>
- [Search Cache Relevance Prompt](references/PROMPTS.md) <br>
- [Jina Reader API endpoint](https://r.jina.ai/) <br>
- [Jina Search API endpoint](https://s.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Search result summaries and structured JSON-like result lists containing titles, URLs, content snippets, source metadata, and optional sentiment scores.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may be cached in a local SQLite database, enriched with extracted page text, and analyzed with configured sentiment or LLM providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
