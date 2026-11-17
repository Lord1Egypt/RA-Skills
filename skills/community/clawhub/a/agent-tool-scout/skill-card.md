## Description:

Agent Tool Scout lets trusted AI agents discover controllable macOS apps, generate CLI wrappers, and execute app commands with structured JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mileszhang001-boom](https://clawhub.ai/user/mileszhang001-boom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let trusted agents discover controllable macOS apps, install generated CLI wrappers, and execute app actions with JSON outputs. It is best suited for local Mac automation workflows where the user can review permissions and approve app actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad local app-control power, including sensitive apps such as Mail, Messages, Finder, Terminal, browsers, office apps, and System Settings.

Mitigation: Use only with trusted agents, approve each app and action, and grant Automation or Accessibility permissions only to a trusted terminal or agent host.

Risk: Security evidence reports a verified AppleScript injection risk involving crafted app or menu metadata.

Mitigation: Avoid scanning or installing wrappers for untrusted local apps, review generated wrappers before use, and limit the skill to known applications.

Risk: Generated commands may vary in reliability across applications and scripting modes.

Mitigation: Use the skill's info and doctor checks before execution, and prefer commands marked as supported.

## Reference(s):

- [Agent Tool Scout on ClawHub](https://clawhub.ai/mileszhang001-boom/skills/agent-tool-scout)
- [mileszhang001-boom ClawHub Publisher Profile](https://clawhub.ai/user/mileszhang001-boom)
- [Project Homepage](https://github.com/mileszhang001-boom/cli-on-mac)
- [PyPI Package](https://pypi.org/project/clam-mac/)
- [Agent Integration Reference](artifact/docs/README-AI.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with osascript and app Automation or Accessibility permissions for many actions.]

## Skill Version(s):

0.1.0 (source: release evidence, SKILL.md frontmatter, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
