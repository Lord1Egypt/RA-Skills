## Description:

AI Product Radar monitors AI product launch signals from RSS feeds, enriches and ranks matching items, captures optional screenshots, and writes trend reports and structured product data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External product, market, and competitive intelligence teams use this skill to monitor AI launch feeds and generate a ranked trend report with structured product data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot capture and custom feed URLs can cause the skill to open untrusted or internal network destinations.

Mitigation: Disable screenshots with `--no-screenshots` for routine use, run screenshot collection in a locked-down sandbox, and validate feed and page URLs to public http/https destinations.

Risk: Unpinned browser tooling can execute code or change behavior during normal execution.

Mitigation: Install and pin Playwright explicitly outside the skill execution path before enabling screenshots.

Risk: Feed content is written into generated HTML and Markdown outputs.

Mitigation: Escape generated HTML and Markdown output before sharing reports or opening generated fallback cards.

## Reference(s):

- [AI Product Radar ClawHub Page](https://clawhub.ai/terrycarter1985/skills/ai-product-radar)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration]

**Output Format:** [Markdown report, JSON data, screenshot files, raw RSS JSON, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces report.md, products.json, screenshots when enabled, and raw/rss_items.json in the configured output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
