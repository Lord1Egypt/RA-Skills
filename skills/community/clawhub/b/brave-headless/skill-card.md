## Description: <br>
Headless web search and content extraction via the Brave Search API, with retry, circuit breaker protection, bounded-concurrency page fetching, structured logging, and paragraph-aware truncation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelexine](https://clawhub.ai/user/kelexine) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill for scriptable web research, documentation lookup, Brave Search result retrieval, and optional extraction of readable Markdown from public web pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Brave Search and requested URLs are fetched from the web. <br>
Mitigation: Avoid confidential queries or internal-only URLs unless authorized, and provide BRAVE_API_KEY only through the environment. <br>
Risk: Query and URL metadata can appear in stderr logs depending on logging settings. <br>
Mitigation: Set LOG_LEVEL and LOG_JSON appropriately for the deployment environment and avoid collecting sensitive logs. <br>
Risk: Extracted web content can be incomplete, stale, or untrusted. <br>
Mitigation: Review extracted Markdown before using it in downstream agent decisions or generated outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kelexine/brave-headless) <br>
- [Skill homepage](https://github.com/kelexine/brave-headless) <br>
- [Brave Search API](https://brave.com/search/api) <br>
- [Architecture reference](ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Plain text or newline-delimited JSON for search results; Markdown or JSON for page extraction.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns up to 20 results; optional content extraction truncates output according to MAX_CONTENT_LENGTH or --max-length.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
