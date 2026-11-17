## Description:

Automates a Douyin content operations pipeline that bootstraps supporting services, rewrites AI and quant finance content, publishes long image-text posts, and replies to comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hnc87](https://clawhub.ai/user/hnc87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to set up and run a Douyin workflow for finding candidate AI and quant finance content, preparing copy, publishing posts, and managing comment replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts and send replies from a logged-in Douyin account.

Mitigation: Use a dedicated account and browser profile, review generated content before live runs, and start with dry-run mode until the posting behavior is understood.

Risk: Setup can clone unpinned GitHub code, install downloaded dependencies, and automatically use available GitHub credentials.

Mitigation: Run in an isolated environment, inspect cloned repositories and dependency files before execution, pin trusted revisions where possible, and avoid exposing GitHub tokens.

Risk: The workflow starts local services, uses a persistent Chrome profile, and sends cover-generation prompts to an external API.

Mitigation: Restrict local service exposure to trusted localhost use, keep the browser profile separate from personal browsing, and review prompts or data before using the external cover-generation API.

## Reference(s):

- [Douyin Automation Skill Page](https://clawhub.ai/hnc87/skills/douyin-auto-hnc)
- [Publishing Rules and Safety Filters](references/publishing.md)
- [Comment Export and Auto Reply](references/comment-reply.md)
- [Qenda AI Cover Generation](references/cover-ai.md)
- [Orchestrator Configuration Reference](references/config-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, service start, pipeline execution, status checks, dry-run mode, AI-disable mode, and optional cron scheduling guidance.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
