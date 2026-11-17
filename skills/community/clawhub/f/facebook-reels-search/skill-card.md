## Description:

Search Facebook Reels by keyword with the official Gecho Bridge MCP tool and return ranked videos, engagement data, details, comments, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to search Facebook Reels by keyword, collect ranked video results, and summarize or save engagement data, comments, details, and links for research and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external MCP package and Chrome extension that operate with a logged-in Facebook browser session.

Mitigation: Install only trusted Gecho Bridge and extension versions, prefer a pinned or reviewed MCP package when possible, and use a dedicated browser profile or account when privacy matters.

Risk: Returned or saved outputs may contain social-media comments, links, engagement data, and other platform-derived content.

Mitigation: Choose a secure writable save directory and review shared outputs for privacy-sensitive or platform-restricted data before distribution.

Risk: Facebook login, CAPTCHA, verification, region, cookie, or blocked-page prompts can interrupt or limit collection.

Mitigation: Resolve browser prompts manually in Chrome before running the workflow and report timeout, empty, or partial results without presenting incomplete enrichment as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/facebook-reels-search)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw setup video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes setup video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with setup commands and structured Facebook Reels result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a local saved result path, partial-result status, enrichment warnings, and summaries of the most useful 3 to 5 returned videos.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
