## Description:

Generate a daily AI news newsletter for a Chinese audience from fresh web sources and return the newsletter body and article summaries in Simplified Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and editorial teams use this skill to gather fresh AI news, filter and verify web results, and produce a daily Simplified Chinese newsletter with structured article metadata and warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, fetched URLs, and page content may be sent to external web search and fetching providers.

Mitigation: Review Brave and Firecrawl privacy terms before use and avoid sensitive queries or URLs.

Risk: Current-news summaries may be incomplete or incorrect when source pages are stale, malformed, inconsistent, or inaccessible.

Mitigation: Review generated warnings and source links before republishing newsletter content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/ai-newsletter-prompt-chn)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [Author link from ClawHub metadata](https://github.com/j3ffyang)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Simplified Chinese Markdown newsletter plus structured JSON containing article summaries, metadata, and warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires web search and web fetch tools with BRAVE_API_KEY and FIRECRAWL_API_KEY configured.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
