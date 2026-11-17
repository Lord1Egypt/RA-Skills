## Description:

Generates technology news digests from RSS, Twitter/X, GitHub, Reddit, web search, and podcast sources with ranking, deduplication, and multi-format output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangwz](https://clawhub.ai/user/tangwz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run automated technology-news digests across built-in and custom sources, then deliver results as Markdown, Discord, email, or PDF reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use authenticated browser tooling through OpenCLI.

Mitigation: Review OpenCLI settings before installation and prefer explicit API tokens or explicitly approved browser-session use.

Risk: OpenCLI may auto-update during a run.

Mitigation: Disable OpenCLI auto-update or pin the approved OpenCLI version before running the skill in managed environments.

Risk: User-configured feed and search URLs can make network requests from the machine running the skill.

Mitigation: Allow only trusted source configuration and review custom sources before execution.

Risk: The advertised built-in source configuration may be unavailable if config/defaults files are missing from the installed artifact.

Mitigation: Verify that the config/defaults files exist in the actual install before relying on built-in sources.

Risk: Optional Python dependencies and external tools affect runtime behavior.

Mitigation: Pin optional Python dependencies and approve optional tools such as OpenCLI, yt-dlp, mail, msmtp, gh, openssl, and weasyprint before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tangwz/skills/follow-news)
- [README](README.md)
- [Digest Prompt](references/digest-prompt.md)
- [Tweet Summarization Reference](references/summarize-tweets.md)
- [Podcast Summarization Reference](references/summarize-podcast.md)
- [Chat Output Template](references/templates/chat.md)
- [Discord Output Template](references/templates/discord.md)
- [Email Output Template](references/templates/email.md)
- [PDF Output Template](references/templates/pdf.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown reports, Discord/email-ready text, JSON pipeline artifacts, and optional PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output can include temporary JSON intermediates, saved digest archives, and source success or failure summaries.]

## Skill Version(s):

3.18.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
