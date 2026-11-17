## Description:

Multi-engine web search (SearXNG) + browsing/scraping (Camofox, CloakBrowser). Use whenever you need to do web research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johell1ns](https://clawhub.ai/user/johell1ns)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform web research across search APIs and browser-based page retrieval, escalating from SearXNG to Camofox or CloakBrowser for dynamic or protected pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security review marked the skill suspicious because it exposes unsafe bypass modes, persistent container setup, and sensitive browser/session controls.

Mitigation: Install only after reviewing the Camofox and CloakBrowser components, avoid unsafe bypass flags and persistent profiles unless needed, pin and verify Docker images, and scope API or admin keys narrowly.

Risk: Browser automation commands can interact with protected sites, proxies, cookies, sessions, screenshots, and local browser services.

Mitigation: Keep browsing services bound locally, avoid placing proxy passwords in commands, close tabs and sessions after use, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johell1ns/skills/browser-search-2)
- [Server-resolved GitHub provenance](https://github.com/Johell1NS/browser-search)
- [Camofox local OpenAPI documentation](http://localhost:9377/openapi.json)
- [Camofox local Swagger UI](http://localhost:9377/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with inline shell commands, API responses, source links, and occasional JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save PNG screenshots when the documented screenshot commands are explicitly used.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
