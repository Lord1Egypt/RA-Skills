## Description: <br>
GEO Optimization helps agents audit and improve content for AI search visibility, LLM discoverability, and citation in AI-powered search experiences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capt-marbles](https://clawhub.ai/user/capt-marbles) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content marketers, SEO/GEO practitioners, and developers use this skill to audit pages, structure content for LLM extraction, and monitor Perplexity citation visibility over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring queries and stored geo-history results may expose confidential strategy, customer names, or unreleased plans to Perplexity or local files. <br>
Mitigation: Use non-confidential test queries unless disclosure is acceptable, and review local geo-history outputs before sharing or committing them. <br>
Risk: The monitoring scripts are preconfigured for Gameye-specific queries, domains, and a hardcoded daily-monitor workspace path. <br>
Mitigation: Edit the queries, domains, and workspace path for the target site before running scheduled monitoring. <br>
Risk: Perplexity monitoring requires an API key and sends prompts to an external API. <br>
Mitigation: Use a scoped Perplexity API key and store it only in the intended local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/capt-marbles/geo-optimization) <br>
- [GEO audit template](references/audit-template.md) <br>
- [Awesome Generative Engine Optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization) <br>
- [Generative Engine Optimization research paper](https://arxiv.org/pdf/2311.09735) <br>
- [Google guidance for succeeding in AI search](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) <br>
- [Schema.org structured data vocabulary](https://schema.org) <br>
- [Perplexity API chat completions endpoint](https://api.perplexity.ai/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, JSON examples, and optional local JSON monitoring reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional monitoring scripts can call Perplexity and write local geo-history JSON summaries when executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
