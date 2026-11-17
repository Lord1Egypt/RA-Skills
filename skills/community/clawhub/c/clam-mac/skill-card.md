## Description:

Give AI hands to control any Mac app. Auto-discover installed apps, generate CLI wrappers, return structured JSON. Works with Music, Finder, Chrome, Word, Figma, and 20+ more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mileszhang001-boom](https://clawhub.ai/user/mileszhang001-boom)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to discover controllable macOS applications, install generated command-line wrappers, execute app actions, and read structured JSON results through shell or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate local macOS applications and may access sensitive personal data through apps such as Mail, Calendar, Reminders, Finder, browsers, and messaging tools.

Mitigation: Grant Automation or Accessibility permissions only for needed apps, review requested actions first, and require explicit confirmation before reading sensitive data, sending messages, moving files, or changing application state.

Risk: The skill installs and delegates execution to the external clam-mac package.

Mitigation: Use a virtual environment, review the installed package source before granting local automation permissions, and avoid persistent MCP or shell configuration changes unless they are required.

Risk: Generated app wrappers can perform destructive or persistent local actions.

Mitigation: Use JSON discovery and doctor checks before execution, prefer read-only commands where possible, and require explicit user approval before deletion, archiving, file moves, sends, or configuration changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mileszhang001-boom/skills/clam-mac)
- [Project homepage](https://github.com/mileszhang001-boom/cli-on-mac)
- [Package on PyPI](https://pypi.org/project/clam-mac/)
- [Issue tracker](https://github.com/mileszhang001-boom/cli-on-mac/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS, osascript, pip, and local Automation or Accessibility permissions for some app actions.]

## Skill Version(s):

0.2.0 (source: SKILL.md frontmatter, pyproject.toml, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
