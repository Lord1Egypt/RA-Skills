## Description:

Smart web search with auto region detection, query intent rewriting, and dual-tier content fetching. Works in both China and international networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run web searches, rewrite search queries for better relevance, and fetch page content from search results across China and international networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs web searches and fetches web pages from the runtime environment, which may expose sensitive search terms or reach internal network resources.

Mitigation: Run it in a contained, low-privilege environment with restricted outbound network access and avoid using sensitive search terms or internal URLs.

Risk: The skill uses browser automation for search and content fetching fallbacks.

Mitigation: Review browser automation behavior before deployment and prefer environments without sensitive developer credentials.

Risk: Dependency setup can install Node packages and Playwright Chromium unless dependencies are already locked and provisioned.

Mitigation: Require locked dependencies and review setup behavior before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/free-smart-web-search)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and command-line output with search result text, links, and fetched page excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include externally fetched web content and search-engine result metadata.]

## Skill Version(s):

2.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
