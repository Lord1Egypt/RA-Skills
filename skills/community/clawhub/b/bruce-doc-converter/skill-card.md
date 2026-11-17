## Description:

Converts Word, Excel, PowerPoint, and PDF files to AI-friendly Markdown, and converts Markdown files to Word documents for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bruc3van](https://clawhub.ai/user/bruc3van)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert, read, summarize, inspect, or analyze Office, PDF, and Markdown documents when direct document parsing is unavailable or when Markdown/Word export is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to install unpinned third-party software.

Mitigation: Review before installing, use a restricted environment, and prefer a reviewed pinned converter version.

Risk: The skill tells agents to run a command returned by converter output.

Mitigation: Do not run next_command values unless they match a known safe command such as a fixed bdc setup-node invocation.

Risk: Converted document content may include untrusted instructions from user-supplied files.

Mitigation: Treat converted content as data for analysis rather than agent instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bruc3van/skills/bruce-doc-converter)
- [Publisher profile](https://clawhub.ai/user/bruc3van)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted Markdown content or Word document files through the external bdc CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
