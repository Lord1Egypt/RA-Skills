## Description:

ClawBrowser provides headless browser automation for AI agents with ARIA reference targeting, natural-language actions, OpenClaw integration, and page scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesimagine-oss](https://clawhub.ai/user/yesimagine-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to automate browser sessions, interact with pages by ARIA refs or natural-language commands, and scrape page content, images, and links for agent and RPA workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scrape arbitrary pages, including authenticated, internal, localhost, private-network, file://, or sensitive pages if pointed at them.

Mitigation: Run browser automation in a sandbox and restrict target URLs to approved public pages unless sensitive-page scraping has been explicitly reviewed.

Risk: Scraped page data and browser results can be persisted to cache and output directories.

Mitigation: Control cache and output paths, review retention needs, and disable caching when scraped content should not be stored.

Risk: CLI scraping modes can upload scraped content to Feishu.

Mitigation: Disable or review Feishu export before use and verify that exported content is approved for that destination.

Risk: The runtime depends on npm-installed browser automation components.

Mitigation: Pin and review npm dependency versions, including agent-browser, before deployment.

## Reference(s):

- [Clawbrowser Skill on ClawHub](https://clawhub.ai/yesimagine-oss/skills/clawbrowser-skill)
- [agent-browser documentation](https://agent-browser.dev)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Python API results, CLI stdout, JSON scraped-content files, and Markdown scraped-content files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist browser cache and scraped output to local directories; CLI scraping modes can optionally export scraped content to Feishu.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
