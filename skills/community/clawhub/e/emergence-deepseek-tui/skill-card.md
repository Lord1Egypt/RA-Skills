## Description:

Use DeepSeek TUI CLI as an autonomous code assistant in two modes: `deepseek exec` for headless, text-in/text-out delegation without filesystem access, and `deepseek run` for interactive coding with filesystem and tool access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to delegate coding tasks to DeepSeek TUI or run DeepSeek TUI interactively for direct code editing, debugging, and command execution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct users to install and run an unpinned third-party autonomous CLI with broad workspace file and shell access.

Mitigation: Use a pinned, reviewed DeepSeek TUI version and run interactive mode only in a limited project directory that excludes unrelated secrets, credentials, and sensitive repositories.

Risk: Headless outputs may include incorrect code, hallucinated APIs, or simulated tool-call text that was not actually executed.

Mitigation: Review generated snippets, ignore simulated tool-call blocks, apply targeted edits manually, and run project build or test checks before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergencescience/skills/emergence-deepseek-tui)
- [DeepSeek TUI GitHub repository](https://github.com/Hmbown/DeepSeek-TUI.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs should be reviewed, scanned, and validated before applying code changes or running commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
