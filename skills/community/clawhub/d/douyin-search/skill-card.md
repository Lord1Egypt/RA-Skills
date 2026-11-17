## Description:

Search Douyin videos from natural-language keywords and return video results or related keyword suggestions when login is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and marketers use this skill to search Douyin for public video content from natural-language Chinese or English requests. It can return structured search results after login or provide related search suggestions without login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reuse persistent browser login cookies, including an existing OpenClaw browser profile.

Mitigation: Require explicit user consent before using saved browser profiles, keep profile directories out of source control, and clear stored cookies when no longer needed.

Risk: The browser automation runs remote Douyin pages with reduced Chromium sandbox isolation.

Mitigation: Avoid running the skill as root, remove --no-sandbox where the environment supports it, and execute searches in a restricted runtime.

Risk: Unpinned browser automation dependencies and Douyin anti-scraping changes can affect reliability and security review outcomes.

Mitigation: Pin dependencies, review updates before deployment, and follow Douyin rate limits and terms of service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/douyin-search)
- [Publisher Profile](https://clawhub.ai/user/terrycarter1985)
- [Douyin](https://www.douyin.com/)
- [Douyin Search Suggestions Endpoint](https://www.douyin.com/aweme/v1/web/search/sug/?keyword=<url-encoded-keyword>&aid=6383)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON search results, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Douyin video URLs, titles, author names, engagement counts, login prompts, or related keyword suggestions.]

## Skill Version(s):

2026.5.10 (source: server release metadata; artifact version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
