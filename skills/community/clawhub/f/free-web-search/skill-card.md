## Description:

Free Web Search lets an agent run Bing China or DuckDuckGo searches with optional page-text fetching and returns structured search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform explicit web searches, route between Bing China and DuckDuckGo, and optionally fetch page text for the first results. It is suited to search-assisted answers where outbound search and geolocation probes are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and IP metadata are sent to external search and geolocation services.

Mitigation: Use the skill only when outbound search is approved and avoid sensitive queries.

Risk: Optional full-page fetch loads arbitrary search results in an unsandboxed browser.

Mitigation: Keep --full at 0 unless page text is needed, and run the skill in an isolated low-privilege environment.

Risk: Dependency setup installs Playwright and Chromium and can use custom package mirrors.

Mitigation: Avoid running setup as root, prefer a virtual environment with pinned dependencies, and use only trusted package mirrors.

## Reference(s):

- [Free Web Search on ClawHub](https://clawhub.ai/ucsdzehualiu/skills/free-web-search)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON array of search results with title, URL, snippet, and optional page text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search result count is capped at 20; optional full-page fetching is capped at 5 results and truncates each page to 8000 characters.]

## Skill Version(s):

8.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
