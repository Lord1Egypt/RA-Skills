## Description:

Fetches article, social post, and general webpage content from supported sites using Playwright, producing structured JSON, screenshots, and downloaded images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gjbmail](https://clawhub.ai/user/gjbmail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations users use this skill to archive or extract web articles, posts, and images from Twitter/X, Zhihu, WeChat public articles, Toutiao, Huxiu, and generic webpages. It is intended for user-authorized and site-compliant content collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use cookie files or browser sessions to access web content.

Mitigation: Run it in an isolated, low-privilege environment and treat cookie files as account credentials.

Risk: The skill accepts broad web targets and can scrape internal or sensitive URLs if pointed at them.

Mitigation: Restrict use to authorized public or approved URLs and avoid internal, private, or sensitive targets.

Risk: Scraped text, screenshots, images, and configuration can remain on disk under the skill directory.

Mitigation: Review and clean fetch_data, cookies, and configuration files after use.

Risk: Some browser launch settings weaken browser security protections to support scraping.

Mitigation: Use a disposable browser context and limit network access to intended targets.

## Reference(s):

- [Troubleshooting Guide](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/gjbmail/skills/content-fetch-skill)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance plus JSON result files, screenshots, and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes task output under fetch_data/{site}/{task_id}/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
