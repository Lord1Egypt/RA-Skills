## Description:

Runs a one-command pipeline that monitors AI product launch signals from RSS feeds, enriches them with web search, captures optional screenshots, scores trends, and writes report and JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and product teams use this skill to monitor recent AI product launches, enrich launch candidates with search context, and produce trend reports for review or downstream automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad outbound web requests to RSS feeds, search providers, and linked pages.

Mitigation: Run it only with trusted feed lists and avoid environments with access to internal services or cloud metadata.

Risk: Screenshot capture renders feed-provided URLs through headless Chromium.

Mitigation: Use --no-screenshots for untrusted feeds or when browser-based page rendering is not required.

Risk: Generated reports, JSON, screenshots, and links may contain untrusted web content.

Mitigation: Treat generated artifacts as untrusted data and review them before using them in agent responses or downstream automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/ai-product-launch-monitor)

## Skill Output:

**Output Type(s):** [markdown, JSON, screenshots, analysis]

**Output Format:** [Markdown report, structured JSON data, and optional PNG screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes report.md, launches.json, and optional screenshots/*.png under the selected output directory.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
