## Description:

Searches Volcengine web and image search APIs so agents can ground answers that depend on current facts, verification, sources, recommendations, prices, comparisons, or other online evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to run web or image searches through Volcengine when answers require fresh information, source links, authority filtering, time ranges, or query rewriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expose API keys by pasting credentials into chat.

Mitigation: Use a dedicated skill credential setting or tightly scoped environment variable; rotate any key already pasted into a conversation.

Risk: Search queries and bearer API keys may be sent to open.feedcoopapi.com in the API-key flow.

Mitigation: Avoid sensitive queries and review the destination and credential handling before installation or use.

Risk: The skill can read legacy OpenClaw .env files, which may contain unrelated secrets.

Mitigation: Run it with isolated environment files and avoid shared .env files that contain credentials for other systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-websearch)
- [Volcengine Web Search API Documentation](https://www.volcengine.com/docs/85508/1650263)
- [Volcengine API Reference](https://www.volcengine.com/docs/87772/2272953)
- [Volcengine Product Introduction](https://www.volcengine.com/docs/87772/2272949)
- [Volcengine Pricing](https://www.volcengine.com/docs/87772/2272951)
- [Docs Index](references/docs-index.md)
- [Setup Guide](references/setup-guide.md)
- [Product Docs Gap Review](references/product-docs-gap.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with search-result summaries, source URLs, image URLs, and command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output may include result counts, latency, titles, site metadata, URLs, summaries, image dimensions, and service error guidance.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
