## Description:

Summarize articles and social posts from URLs using full-content retrieval first, with browser fallback when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khalilhsu](https://clawhub.ai/user/khalilhsu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize public articles, social posts, and visible comment discussions while clearly reporting access or completeness limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch or render URLs supplied by the user, including through web retrieval, a Jina mirror fallback, and browser interaction.

Mitigation: Use it for public pages by default and avoid private, account-specific, or sensitive URLs unless that retrieval behavior is acceptable.

Risk: Some pages may expose only partial content because of paywalls, login requirements, verification pages, dynamic rendering, or inaccessible comments.

Mitigation: Summarize only visible content and clearly label access or completeness limitations instead of guessing.

## Reference(s):

- [Article Summarizer ClawHub Page](https://clawhub.ai/khalilhsu/skills/article-summarizer-plus)
- [Output Patterns](artifact/references/output-patterns.md)
- [Retrieval Playbook](artifact/references/retrieval-playbook.md)
- [Source Notes](artifact/references/source-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise summaries by default, with optional sections for notable details, takeaways, and visible comment themes when requested or relevant.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
