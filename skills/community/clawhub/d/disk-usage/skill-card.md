## Description:

Shows human-readable disk usage for a requested directory or path using the system du command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinwangmok](https://clawhub.ai/user/jinwangmok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and external users can use this skill when they need an agent to check human-readable disk usage for a directory or path during maintenance, cleanup, or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect precise file-size support because some artifact text describes a file or directory, while server security guidance says to treat the package as a directory-usage tool rather than a reliable file-size tool.

Mitigation: Use it primarily for directory usage checks, and verify file-size needs with a dedicated command when exact single-file behavior matters.

Risk: The agent may run du on paths supplied by the user, which can reveal directory names and size information from the selected location.

Mitigation: Run the skill only on paths the user intentionally requests and is authorized to inspect.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinwangmok/skills/disk-usage)
- [Publisher profile](https://clawhub.ai/user/jinwangmok)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human-readable size output; the bundled script lists up to 20 largest immediate directory children followed by the selected directory total.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
