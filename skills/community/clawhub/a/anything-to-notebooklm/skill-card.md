## Description:

Converts WeChat articles, webpages, YouTube videos, PDFs, Markdown, and other sources into NotebookLM sources and generated outputs such as podcasts, slides, mind maps, reports, quizzes, and flashcards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonicbotman](https://clawhub.ai/user/sonicbotman)

### License/Terms of Use:

MIT-0

## Use Case:

External Claude Code users use this skill to gather content from web, file, and search sources, upload it to NotebookLM, and request generated study or presentation materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation pulls and runs unpinned third-party GitHub code and dependencies.

Mitigation: Review the MCP server source and dependency revisions first, pin trusted revisions where possible, and install in a virtual environment.

Risk: The skill uploads selected or extracted content to Google NotebookLM.

Mitigation: Avoid sensitive, private, or copyrighted files unless upload is intentional and permitted.

Risk: The skill adds a persistent MCP server to Claude configuration.

Mitigation: Review the configuration entry before enabling it and remove or disable the MCP server when it is not needed.

Risk: Troubleshooting guidance includes changing /tmp permissions.

Mitigation: Do not run the /tmp permission troubleshooting command; use least-privilege, directory-specific fixes instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sonicbotman/skills/anything-to-notebooklm)
- [Project homepage](https://github.com/joeseesun/anything-to-notebooklm)
- [Google NotebookLM](https://notebooklm.google.com/)
- [Microsoft markitdown](https://github.com/microsoft/markitdown)
- [wexin-read-mcp](https://github.com/Bwkyd/wexin-read-mcp)
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files such as MP3, PDF, JSON, Markdown, text, PNG, or MP4 through NotebookLM workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
