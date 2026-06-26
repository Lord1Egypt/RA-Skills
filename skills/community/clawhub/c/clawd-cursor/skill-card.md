## Description: <br>
ClawdCursor lets an OpenClaw agent operate visible Windows or macOS desktop applications through a local Clawd Cursor API when direct tools are not enough. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmrDab](https://clawhub.ai/user/AmrDab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route user-approved desktop or browser UI tasks to Clawd Cursor after direct API, CLI, filesystem, or browser-native tools have been tried. It is intended for GUI interaction, visual verification, form filling, and cross-application workflows on the user's own machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad ability to see and operate the user's desktop, including sensitive applications. <br>
Mitigation: Use it only for intentional desktop tasks, prefer direct tools when available, and require user confirmation before sensitive apps, messages, deletions, purchases, account changes, or settings changes. <br>
Risk: Starting the local service can make screen-control capability available before the user expects it. <br>
Mitigation: Start Clawd Cursor only when it is explicitly needed, keep the service bound to localhost, review the external repository before setup, and stop or abort tasks when work is complete. <br>
Risk: Screenshots and UI text may be sent to the user's configured cloud AI provider when local mode is not used. <br>
Mitigation: Prefer local/Ollama mode for private screens and avoid exposing credentials, private messages, financial data, or other sensitive content unless the user has clearly approved that data flow. <br>


## Reference(s): <br>
- [ClawdCursor on ClawHub](https://clawhub.ai/AmrDab/clawd-cursor) <br>
- [Clawd Cursor homepage](https://clawdcursor.com) <br>
- [Clawd Cursor source repository](https://github.com/AmrDab/clawd-cursor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell, PowerShell, JavaScript, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to poll local task status, request user approval for safety-gated actions, and prefer direct tools before GUI automation.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
