## Description: <br>
Top-level Windows computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to build and run a Windows-only computer-use MCP server that gives an agent screenshots, mouse, keyboard, app launch, app/window inspection, display mapping, and clipboard access through a bundled standalone runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Windows desktop, screenshot, app, keyboard, mouse, and clipboard authority without a real user approval step. <br>
Mitigation: Run it only in a dedicated VM or non-sensitive Windows profile, close secrets and private documents before use, and avoid machines with production access, financial accounts, or privileged sessions. <br>
Risk: The runtime bootstraps dependencies on first run through npm and pip package installation. <br>
Mitigation: Review the dependency bootstrap path and package sources before first use in controlled environments. <br>
Risk: The artifact states that end-to-end runtime behavior still needs validation on a real Windows machine. <br>
Mitigation: Validate GUI control, screenshot capture, UAC, elevated windows, secure desktop transitions, mixed-DPI multi-monitor behavior, and focus boundaries before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/computer-use-windows) <br>
- [GitHub repository](https://github.com/wimi321/windows-computer-use-skill) <br>
- [Project README](project/README.md) <br>
- [MCP configuration example](project/examples/mcp-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only MCP setup guidance; first run may bootstrap public npm and pip dependencies.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
