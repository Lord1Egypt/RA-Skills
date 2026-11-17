## Description:

Browse and read articles and podcasts from Elsewhere (elsewhere.news), a media platform featuring original, first-hand stories from China's tech and startup ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pitayak](https://clawhub.ai/user/pitayak)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse Elsewhere articles and podcasts, rank them against the user's interests, and return concise recommendations, summaries, and source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad personal context and creates or updates a persistent local preference profile.

Mitigation: Limit personalization inputs to what the user has agreed to share, make profile storage visible and editable, and avoid pre-filling preferences without evidence.

Risk: The skill can fetch mutable remote instructions before use.

Mitigation: Pin reviewed instructions by version or hash and require review before adopting remote changes.

Risk: The skill can be configured for recurring daily background browsing.

Mitigation: Enable scheduled runs only after explicit opt-in and keep the schedule easy to change or disable.

Risk: The skill can send public article-like requests to Elsewhere.

Mitigation: Require confirmation before external state-changing actions or disable automated likes by default.

Risk: The skill treats missing user response as recommendation feedback.

Mitigation: Avoid interpreting silence as a strong preference signal unless the user has agreed to that feedback model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pitayak/skills/elsewhere-news)
- [Elsewhere site overview](https://elsewhere.news/llms.txt)
- [Elsewhere RSS feed](https://elsewhere.news/feed.xml)
- [Elsewhere public API](https://elsewhere.news)
- [TASTE.md specification](https://elsewhere.news/specs/taste)
- [llms.txt standard](https://llmstxt.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations, summaries, and links with optional shell command snippets or configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update a local TASTE.md preference profile and may suggest scheduled daily browsing when the user opts in.]

## Skill Version(s):

1.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
