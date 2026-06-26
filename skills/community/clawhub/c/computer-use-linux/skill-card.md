## Description: <br>
Top-level Linux computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add Linux desktop control through a standalone MCP server, including screenshots, mouse and keyboard input, app and window inspection, app launch, and clipboard workflows on trusted local Linux sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose unredacted screen contents and operate mouse, keyboard, app launch, and clipboard functions in a local desktop session. <br>
Mitigation: Use it only on trusted Linux desktops, avoid sensitive apps and private data during sessions, and keep requested app and clipboard access narrowly scoped. <br>
Risk: The standalone runtime auto-grants powerful screen, input, app, and clipboard permissions without a real user approval step. <br>
Mitigation: Review or change the auto-approval behavior before use, especially in shared, production, or sensitive environments. <br>
Risk: First run can create a Python virtual environment and install runtime dependencies. <br>
Mitigation: Review the bundled dependency list and run installation in an environment where first-run package installation is expected and permitted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wimi321/computer-use-linux) <br>
- [Publisher profile](https://clawhub.ai/user/wimi321) <br>
- [Bundled README](artifact/project/README.md) <br>
- [MCP configuration example](artifact/project/examples/mcp-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces build and run guidance for a Linux-only standalone MCP server that may bootstrap a Python virtual environment on first launch.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
