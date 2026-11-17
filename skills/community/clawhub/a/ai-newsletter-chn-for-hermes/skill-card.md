## Description:

Generate a daily AI news newsletter for a Chinese audience from fresh web sources, returning the newsletter body and article summaries in Simplified Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to curate current AI and machine learning news into a daily Simplified Chinese newsletter with source links, summaries, article metadata, and warnings for skipped or inconsistent results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newsletter content depends on live web search and fetched pages, so articles may be unavailable, stale, or mismatched.

Mitigation: Use the skill's verification flow, review warnings, and confirm important items against their source links before publication.

Risk: The skill requires Brave and Firecrawl API keys for web search and fetching.

Mitigation: Provide only scoped keys through the host environment and rotate or revoke them according to local policy.

Risk: Output is in Simplified Chinese by default, which may not match every audience or locale.

Mitigation: Confirm the target audience and adapt the newsletter before reuse in another locale.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/ai-newsletter-chn-for-hermes)
- [Publisher profile](https://clawhub.ai/user/j3ffyang)
- [Author link from metadata](https://github.com/j3ffyang)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Simplified Chinese newsletter text plus Markdown and JSON newsletter outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source metadata including title, URL, domain, published date, relevance score, source query, and warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
