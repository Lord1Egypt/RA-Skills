## Description: <br>
ClawdCursor is an OS-level desktop automation tool server that exposes 42 tools for controlling applications on Windows, macOS, and Linux via REST or MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrdab](https://clawhub.ai/user/amrdab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ClawdCursor as a fallback path for GUI and desktop tasks when native APIs, CLIs, direct file edits, or browser automation are not available. The skill helps an agent inspect screens, control windows, type, click, run browser CDP actions, and delegate complex local desktop workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad local desktop control, including actions in arbitrary applications. <br>
Mitigation: Install only when desktop control is intentionally needed, review and pin the package before installation, and keep the server stopped when not in use. <br>
Risk: The documented install flow uses an unpinned external package install and pre-accepts consent. <br>
Mitigation: Do not let an agent casually accept consent or start the server; require a human to review the package and approve startup. <br>
Risk: Bearer-token access can authorize local desktop actions if the token is exposed. <br>
Mitigation: Keep the bearer token private and limit use to the local 127.0.0.1 server. <br>
Risk: Desktop automation may send, delete, purchase, transfer funds, post publicly, or change accounts. <br>
Mitigation: Require explicit human approval before sends, deletes, purchases, transfers, password-manager use, public posts, and account changes. <br>


## Reference(s): <br>
- [ClawdCursor Homepage](https://clawdcursor.com) <br>
- [ClawdCursor Source Repository](https://github.com/AmrDab/clawdcursor) <br>
- [ClawHub Release Page](https://clawhub.ai/amrdab/clawdcursor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Code] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local REST or MCP calls and desktop-control actions that require explicit user consent and approval for high-impact operations.] <br>

## Skill Version(s): <br>
0.7.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
