## Description:

Generate a daily AI news newsletter for a Chinese audience from fresh web sources, summarizing current AI/ML articles into Markdown and JSON with Simplified Chinese output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to curate recent AI/ML news into a daily Simplified Chinese newsletter with source links and a matching JSON payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses configured Brave and Firecrawl credentials to search and fetch public web pages.

Mitigation: Install it only in environments where those credentials are intended for agent use, and do not expose secrets in prompts or generated output.

Risk: The skill is designed for Simplified Chinese AI-news digests and may not fit other languages or non-news tasks without edits.

Mitigation: Use it for current AI/ML newsletter generation as documented, and modify the skill before applying it to other languages or task types.

Risk: Generated summaries depend on current public web sources and may reflect missing dates, fetch failures, or source inconsistencies.

Mitigation: Review source links, warnings, and article metadata before republishing the newsletter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/ai-newsletter-chn)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Simplified Chinese Markdown newsletter plus structured JSON object.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes article titles, URLs, domains, publication dates, summaries, relevance scores, source queries, and warnings.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
