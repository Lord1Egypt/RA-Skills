## Description:

Gemini Deep Research runs a Gemini CLI deep-research MCP workflow for deep topic research, market or industry analysis, and comprehensive report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to delegate long-running Gemini Deep Research tasks, choose a report format, and save the resulting research report to disk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and report parameters are sent to Gemini through a third-party deep-research extension.

Mitigation: Avoid sensitive topics or secrets unless the organization permits that data flow.

Risk: The local extension can change over time when auto-update is enabled.

Mitigation: Pin the extension to a reviewed version and disable auto-update before use in controlled environments.

Risk: The workflow writes generated reports to disk.

Mitigation: Restrict output paths to a dedicated reports folder and review saved content before sharing.

## Reference(s):

- [Gemini Deep Research Setup Guide](references/setup-guide.md)
- [gemini-cli-deep-research extension](https://github.com/allenhutchison/gemini-cli-deep-research)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research report saved to a file, with JSON status output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Comprehensive Research Report, Executive Brief, and Technical Deep Dive formats; default timeout is 15 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
