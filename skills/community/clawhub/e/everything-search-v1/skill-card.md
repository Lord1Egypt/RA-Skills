## Description:

Everything-Search-Skill helps agents search local file names, paths, extensions, and sizes on Windows 10/11 or WSL2 through the Everything es.exe CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1tokener](https://clawhub.ai/user/1tokener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to locate local files by name, path, extension, or size without performing full-text or web search. It is intended for Windows 10/11 and WSL2 environments where Everything and its es.exe CLI are available or can be configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke Everything/es.exe, automatically start Everything, and persist executable paths during normal searches without a clear confirmation step.

Mitigation: Review and pin ES_PATH and EVERYTHING_PATH before use; add explicit confirmation and trusted-path validation in managed or sensitive environments.

Risk: Search output may expose local file names, paths, sizes, and extensions to the active agent session.

Mitigation: Use the skill only where sharing local file metadata with the agent is acceptable, and review outputs before including them in broader conversation context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1tokener/skills/everything-search-v1)
- [Server-resolved GitHub provenance](https://github.com/1TOKENer/Everything-Search-Skill)
- [Everything command line interface documentation](https://www.voidtools.com/zh-cn/support/everything/command_line_interface/)
- [Everything command line options documentation](https://www.voidtools.com/zh-cn/support/everything/command_line_options/)
- [Everything search syntax documentation](https://www.voidtools.com/support/everything/searching/)
- [Everything es.exe download](https://www.voidtools.com/zh-cn/downloads/#cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style terminal output with tabular search results and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped by the script max_results parameter, defaulting to 100.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
