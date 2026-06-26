## Description: <br>
Top-level macOS computer-use skill with a bundled standalone runtime that bootstraps itself without any local Claude installation, private native modules, or extracted app assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and run a portable macOS computer-use MCP server for screenshots, mouse and keyboard input, app inspection, clipboard access, and desktop automation in trusted local sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables real macOS desktop control and requires Accessibility and Screen Recording access. <br>
Mitigation: Install only in trusted local sessions, review the source first, and avoid exposing sensitive windows or clipboard contents while the agent is operating the desktop. <br>
Risk: The security evidence says the standalone permission flow auto-grants requested app and clipboard/system-key flags rather than asking each time. <br>
Mitigation: Use explicit human oversight for sessions that invoke computer-use tools and restrict use to workflows where agent desktop operation is intended. <br>
Risk: The runtime reports screenshotFiltering: none, so screenshot capture is not compositor-filtered. <br>
Mitigation: Close or hide sensitive applications before use and verify MCP-layer allowlist, tier, and action gates before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wimi321/computer-use-macos) <br>
- [Skill README](artifact/project/README.md) <br>
- [MCP configuration example](artifact/project/examples/mcp-config.json) <br>
- [Python runtime requirements](artifact/project/runtime/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [macOS-only computer-use workflow guidance and MCP server configuration.] <br>

## Skill Version(s): <br>
0.2.2 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
