## Description:

Fetch and extract clean article content from any URL using the Diffbot Article API. Returns clean Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve the main content and article metadata from public article, blog post, or news URLs as clean Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested article URLs and the Diffbot API token are sent to Diffbot as part of normal operation.

Mitigation: Use the skill only for links where sharing with Diffbot is intended and allowed; avoid private, internal, authenticated, or sensitive URLs unless policy permits that sharing.

## Reference(s):

- [Diffbot Article API endpoint](https://api.diffbot.com/v3/article)
- [ClawHub skill page](https://clawhub.ai/flobo3/skills/diffbot-fetch)
- [Publisher profile](https://clawhub.ai/user/flobo3)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown article content with title and optional author, date, and site metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a URL input and DIFFBOT_API_KEY; the requested URL is sent to Diffbot for article extraction.]

## Skill Version(s):

1.0.0 (source: server release evidence, released 2026-03-31)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
