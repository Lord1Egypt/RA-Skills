## Description:

Generate a daily AI news newsletter from fresh web sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and AI practitioners use this skill to produce current AI news roundups from fresh web sources. It is intended for daily digests, curated newsletters, briefings, and practitioner-relevant AI developments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated summaries may reflect stale, incomplete, or mismatched web pages from external sources.

Mitigation: Review generated links and summaries as editorial output before publication.

Risk: The skill uses configured Brave and Firecrawl credentials to search and fetch external web pages.

Mitigation: Provide credentials only through environment variables and do not expose secret values in prompts or generated output.

Risk: Fetched article text may be copyrighted or unsuitable for republication in full.

Mitigation: Use concise factual summaries and source links rather than reproducing full article text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/ai-newsletter)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured response containing newsletter_items, markdown_newsletter, and json_newsletter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source URLs, publication metadata when available, relevance scores, and actionable warnings for fetch or validation issues.]

## Skill Version(s):

1.3.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
