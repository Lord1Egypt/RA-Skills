## Description:

Multi-source deep research agent that searches the web, synthesizes findings, and delivers cited reports using Tavily API when available or DuckDuckGo as a fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan multi-source web research, inspect key sources, and synthesize cited reports for decision support, learning, or writing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary web pages during research.

Mitigation: Run it in a constrained environment where web access is acceptable and avoid private or internal URLs.

Risk: Research queries may be sent to Tavily when the API key is configured.

Mitigation: Treat Tavily as an external API dependency and avoid sensitive or confidential queries unless that use is approved.

Risk: The artifact workflow saves reports to disk by default.

Mitigation: Prefer opt-in saving with a user-approved output path before writing report files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/deep-research-pro-litiao)
- [Tavily](https://tavily.com)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with citations, summaries, source lists, methodology notes, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports to disk as Markdown or JSON when the agent follows the artifact workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
