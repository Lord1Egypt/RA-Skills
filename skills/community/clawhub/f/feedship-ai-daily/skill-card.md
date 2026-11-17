## Description:

Generate daily AI news digest from feedship subscriptions by extracting articles, filtering AI and technology content, generating strategic analysis with an LLM, and replacing citation placeholders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanpeipan](https://clawhub.ai/user/yanpeipan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw-compatible agent users use this skill to produce an AI-focused daily news briefing from local Feedship subscriptions, either on demand or through a scheduled daily run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring schedule can run the digest automatically before the user has reviewed operational settings.

Mitigation: Review the cron schedule, timezone, destination, timeout, and isolated-session settings before enabling automatic runs.

Risk: Generated summaries and links are derived from feed content that may be untrusted or misleading.

Mitigation: Treat generated reports as untrusted until article content, links, and summaries have been reviewed for accuracy and safe URL schemes.

Risk: The workflow uses fixed files under /tmp for intermediate article and report data.

Mitigation: Run the skill in an isolated account or session and prefer private temporary paths when adapting the workflow.

## Reference(s):

- [Prompt Template](references/prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/yanpeipan/skills/feedship-ai-daily)
- [Publisher Profile](https://clawhub.ai/user/yanpeipan)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with injected article citation links and supporting shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports on-demand execution and an optional daily cron schedule; requires uv and Feedship v1.8.0 or newer.]

## Skill Version(s):

1.21.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
