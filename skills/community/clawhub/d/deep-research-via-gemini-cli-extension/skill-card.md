## Description:

Execute Gemini Deep Research using the gemini-deep-research MCP extension for the Gemini CLI for comprehensive research on market, industry, geopolitical, investment, or other complex multi-source topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to start, monitor, and save Gemini Deep Research reports from an agent session. It is intended for deep, multi-source research workflows where the user confirms topic, report format, output path, and polling duration before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on third-party Gemini extension code that may auto-update and execute locally with the user's permissions.

Mitigation: Pin and review the extension version before use, and disable auto-update where possible.

Risk: Detached background polling jobs can continue running after the agent exits and can access local files and Google research data.

Mitigation: Run only on trusted machines, monitor the task directory, and avoid sensitive research topics on shared systems.

Risk: Task files and report output paths have limited containment.

Mitigation: Use a dedicated report directory and review task.json and output paths before starting research.

## Reference(s):

- [Gemini Deep Research Setup Guide](references/setup-guide.md)
- [Gemini CLI Deep Research Extension](https://github.com/allenhutchison/gemini-cli-deep-research)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [NotebookLM](https://notebooklm.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON status messages, shell commands, and task configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Comprehensive Research Report, Executive Brief, and Technical Deep Dive formats; background polling defaults to eight five-minute polling attempts.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
