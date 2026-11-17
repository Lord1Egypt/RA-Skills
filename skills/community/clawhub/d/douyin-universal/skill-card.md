## Description:

Searches and collects Douyin content, including video search results, user videos, video metadata, comments, and optional video downloads, using HTTP APIs and agent-browser for logged-in comment harvesting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[excalibursssooo](https://clawhub.ai/user/excalibursssooo)

### License/Terms of Use:

MIT

## Use Case:

External users, researchers, and developers use this skill for small-scale Douyin content research, trend discovery, comment collection, aggregation, and local export of results. It is not positioned for large-scale scraping services or 24/7 monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses full Douyin login cookies and authenticated browser state for comment harvesting.

Mitigation: Create cookie files locally, avoid pasting credentials into chat, store credentials outside committed files when possible, restrict file permissions, and remove stale session data when no longer needed.

Risk: Generated CSV and JSON exports may contain untrusted user-supplied content from Douyin.

Mitigation: Treat exported data as untrusted input, inspect it before reuse, and avoid directly executing or importing generated values into downstream systems.

Risk: Scraping and downloading Douyin content may violate service terms, privacy obligations, rate limits, or content rights if misused.

Mitigation: Use the skill only for compliant small-scale research or analysis, respect platform terms and applicable data protection laws, and avoid commercial resale or unauthorized republication of collected content.

Risk: Aggressive or large-scale collection can trigger anti-abuse controls and is outside the documented operating posture.

Mitigation: Prefer the default lower-risk mode, keep harvesting serial, limit volume, and stop when cookies expire, captcha appears, or the scripts report authentication failures.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/excalibursssooo/skills/douyin-universal)
- [Publisher Profile](https://clawhub.ai/user/excalibursssooo)
- [README](README.md)
- [Developer Pitfalls](docs/pitfalls.md)
- [agent-browser](https://github.com/vercel-labs/agent-browser)
- [Douyin](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, CSV, Files]

**Output Format:** [Markdown guidance with shell commands; runtime scripts emit JSON, CSV, and local video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and agent-browser; comment harvesting requires a locally managed Douyin cookie file or browser state.]

## Skill Version(s):

1.2.0 (source: frontmatter and changelog, released 2026-06-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
