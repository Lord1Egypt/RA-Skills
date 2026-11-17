## Description:

Triggers Gemini Deep Research through an OpenClaw browser session, extracts the completed report, and exports it as a formatted Notion page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palmpalm7](https://clawhub.ai/user/palmpalm7)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to run a Gemini Deep Research workflow from a logged-in browser session and publish the resulting research report to a configured Notion page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's logged-in Gemini browser profile and local Notion token.

Mitigation: Install only in an environment where that browser profile and token are intended for agent use.

Risk: The skill exports full reports to a hard-coded Notion destination without a built-in confirmation step.

Mitigation: Replace and verify the Notion parent page ID, restrict the Notion integration to the intended page, and add review before export for sensitive topics.

Risk: The skill temporarily saves full research reports under /tmp.

Mitigation: Avoid sensitive research topics unless temporary files are reviewed, protected, or removed after use.

## Reference(s):

- [Gemini app](https://gemini.google.com/app)
- [Notion pages API](https://api.notion.com/v1/pages)
- [ClawHub skill page](https://clawhub.ai/palmpalm7/skills/gemini-deep-research-notion)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown report text, Notion blocks, status updates, and a Notion page URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Gemini browser profile, a local Notion API key, and a configured Notion parent page.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
