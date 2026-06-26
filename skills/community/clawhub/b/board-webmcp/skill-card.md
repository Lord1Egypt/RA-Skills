## Description: <br>
Connect to the native board demo through local-mcp and one fixed UXC link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, edit, lay out, and export the shared board at board.holon.run or a local board instance through browser WebMCP. It supports collaborative visible sessions when a human is editing or reviewing the same board. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can visibly edit a shared demo board and persist changes in the configured browser profile. <br>
Mitigation: Use it deliberately, read or export the board before edits, and confirm before making visible collaborative changes. <br>
Risk: Shared board sessions may expose information placed on the board to other collaborators. <br>
Mitigation: Keep the dedicated browser profile isolated and avoid placing secrets or sensitive data on the shared board. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Board Webmcp ClawHub release](https://clawhub.ai/jolestar/board-webmcp) <br>
- [Default public board target](https://board.holon.run) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that may visibly edit or export a shared board; JSON output is recommended for automation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
