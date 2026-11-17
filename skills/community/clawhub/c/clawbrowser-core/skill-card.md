## Description:

Headless browser automation CLI for ARIA ref-based element selection, natural language actions, and OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesimagine-oss](https://clawhub.ai/user/yesimagine-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, inspect accessibility-tree snapshots, interact with page elements by stable refs, and scrape page text, images, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scrape browser content from pages the agent can access.

Mitigation: Run it only against intended public or approved targets, and avoid private, internal, or authenticated pages unless scraping is explicitly authorized.

Risk: Scraped content may be persisted to local JSON and Markdown archives.

Mitigation: Use a sandboxed account or container, review output directories, and clear caches or archives after use when content is sensitive.

Risk: The scraper CLI can upload scraped content to Feishu.

Mitigation: Do not use the web_scraper CLI or save_to_feishu option unless external upload is acceptable for the target content.

## Reference(s):

- [Clawbrowser Skill Release](https://clawhub.ai/yesimagine-oss/skills/clawbrowser-core)
- [agent-browser documentation](https://agent-browser.dev)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, Python code examples, shell commands, and browser/scraper result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON and Markdown scrape archives when the web_scraper utility is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
