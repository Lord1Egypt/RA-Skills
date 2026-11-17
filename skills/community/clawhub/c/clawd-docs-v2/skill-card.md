## Description:

Smart ClawdBot documentation access with local search index, cached snippets, and on-demand fetch. Token-efficient and freshness-aware.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aranej](https://clawhub.ai/user/aranej)

### License/Terms of Use:


## Use Case:

Developers and ClawdBot users use this skill to answer ClawdBot documentation questions by checking local snippets and indexes first, then fetching official documentation pages when local evidence is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local ClawdBot documentation files under ~/clawd/data and fetch pages from docs.clawd.bot when local snippets or cache entries are insufficient.

Mitigation: Prefer local snippets and index matches first, and review fetched documentation paths before using the returned guidance.

Risk: Minor wording inconsistencies in the artifact may confuse whether to check a cache or refresh from the web.

Mitigation: Clarify cache-check and fetch steps before deployment, and verify freshness when documentation age affects the answer.

## Reference(s):

- [ClawdBot Documentation](https://docs.clawd.bot/)
- [ClawdBot Skills Documentation](https://docs.clawd.bot/tools/skills)
- [ClawdBot Multi-Agent Documentation](https://docs.clawd.bot/concepts/multi-agent)
- [ClawdBot Documentation Index](https://docs.clawd.bot/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritizes cached snippets and local documentation indexes before fetching official ClawdBot documentation pages.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
