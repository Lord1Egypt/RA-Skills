## Description:

Summarize or extract text/transcripts from URLs, podcasts, and local files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize web pages, podcasts, local documents, and YouTube or video links, or to extract best-effort transcripts when source media supports it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted files, private URLs, or transcripts may be sent to the selected model provider or optional extraction services.

Mitigation: Avoid using the skill with confidential or sensitive content unless the selected provider and optional services are approved for that data.

Risk: The skill requires installing and trusting the summarize CLI and its Homebrew tap.

Mitigation: Review the CLI and installation source before deployment, and install only in environments where that dependency is trusted.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/content-summarizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summaries or extracted text, with optional JSON output when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output length and extraction behavior can be adjusted with CLI flags such as length, max output tokens, extract-only, JSON, Firecrawl, and YouTube options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
