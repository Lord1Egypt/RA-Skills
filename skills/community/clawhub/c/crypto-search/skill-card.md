## Description:

Searches and synthesizes cryptocurrency-related content from Twitter/X and News using Kaito MCP search, with guidance for exact-match, boolean, topic, token, and username queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yh9277](https://clawhub.ai/user/yh9277)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to retrieve and summarize crypto-related Twitter/X and News content by token, keyword, indexed topic, or username.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Kaito MCP and may retrieve public Twitter/X and News results.

Mitigation: Review requested queries before execution, especially when prompts are vague or may contain sensitive context.

Risk: The skill depends on exact-match and boolean search behavior, so poorly structured queries can miss relevant content or over-narrow results.

Mitigation: Use one entity field per call, apply boolean expansion for variants, and cite only claims present in retrieved results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yh9277/skills/crypto-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with source links and smart_engagement counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return structured search results when composed into higher-level workflow skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
