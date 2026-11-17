## Description:

Searches Douyin, Xiaohongshu, and Bilibili for user-provided terms and returns summarized search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiao4d-lyf](https://clawhub.ai/user/xiao4d-lyf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Chinese social-media platforms for a topic and summarize returned video or note results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided search strings may be inserted into command templates unsafely.

Mitigation: Review commands before execution and use safe argument handling or URL encoding for search terms.

Risk: Search terms are sent to third-party social-media platforms.

Mitigation: Avoid sensitive search terms and confirm the user is comfortable opening Douyin, Xiaohongshu, or Bilibili before searching.

Risk: Results may be incomplete when a platform requires login or changes its page structure.

Mitigation: Check for login prompts or failed selectors and ask the user to authenticate or re-run discovery when results do not load.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiao4d-lyf/skills/cn-social-media-search)
- [Douyin](https://www.douyin.com)
- [Xiaohongshu](https://www.xiaohongshu.com)
- [Bilibili Search](https://search.bilibili.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with inline OpenClaw browser commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results depend on target site availability, login state, and current page structure.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact version history, released 2026-04-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
