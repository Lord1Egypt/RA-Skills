## Description:

Generative Engine Optimization (GEO) for AI search visibility. Optimize content to appear in ChatGPT, Perplexity, Claude, and Google AI Overviews. Use when optimizing websites, pages, or content for LLM discoverability and citation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

External marketers, content teams, and developers use this skill to audit pages for AI-search visibility, structure pages for LLM citation, and monitor Perplexity citation behavior over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Perplexity-backed monitoring sends configured test queries to a third-party API and saves responses locally.

Mitigation: Review queries for sensitive data, use approved API credentials only, and document local retention before running monitoring.

Risk: The automation broadly loads .env values and can expose unrelated local secrets to the script environment.

Mitigation: Restrict environment loading to PERPLEXITY_API_KEY or run in a clean environment with only the required secret.

Risk: Cron-style monitoring and fixed local paths may run in the wrong workspace or persist beyond intended testing.

Mitigation: Replace hardcoded paths, use explicit working directories, and review scheduled jobs before enabling automation.

Risk: The shell wrapper writes to a fixed /tmp path and embeds filenames into inline Python source.

Mitigation: Use unique temporary files and avoid interpolating filenames into inline Python.

## Reference(s):

- [GEO Audit Template](references/audit-template.md)
- [ClawHub skill page](https://clawhub.ai/capt-marbles/skills/geo-optimization)
- [Awesome Generative Engine Optimization](https://github.com/amplifying-ai/awesome-generative-engine-optimization)
- [Princeton GEO Research Paper](https://arxiv.org/pdf/2311.09735)
- [Google AI Search Guidance](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search)
- [Perplexity Ranking Factors](https://firstpagesage.com/seo-blog/perplexity-ai-optimization-ranking-factors-and-strategy/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, JSON query files, and shell or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitoring scripts may save Perplexity query results and summary JSON under geo-history when run.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
