## Description:

Free Web Search Js searches the web with Playwright and HTTP, using Bing CN or DuckDuckGo and optionally fetching page content without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to look up current web information, fact-check claims, find documentation or tutorials, and fetch page text for downstream reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary HTTP URLs from the agent runtime, which can expose internal, localhost, cloud metadata, or private-network endpoints if misused.

Mitigation: Use it in an isolated environment with restricted network access, avoid sensitive URLs, and prefer explicit --region plus --no-fetch when privacy matters.

Risk: The skill may run untrusted pages in Chromium while default browser launch flags disable the browser sandbox.

Mitigation: Update Playwright before sensitive use and remove the default no-sandbox browser flags on hosts where browser isolation matters.

Risk: Queries, fetched URLs, and page requests are sent directly to search engines and target websites from the runtime.

Mitigation: Do not submit confidential queries or URLs, and review fetched content before relying on it in downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/free-web-search-js)
- [ClawHub publisher profile](https://clawhub.ai/user/ucsdzehualiu)
- [Node.js](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [JSON containing search results, URLs, snippets, and fetched page text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count and per-page content length are configurable; search may auto-fetch top results unless disabled.]

## Skill Version(s):

29.1.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
