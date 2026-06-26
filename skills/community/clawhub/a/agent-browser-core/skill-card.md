## Description: <br>
OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to plan and operate browser automation workflows with the agent-browser CLI, using snapshots, element refs, structured commands, and approval guardrails for sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can interact with authenticated pages, local files, downloads, or network traffic when sensitive options are enabled. <br>
Mitigation: Run the CLI in a low-privilege dedicated environment, allowlist target sites, block private network targets, and require human approval for eval, file access, downloads, proxies, traffic interception, and credential or session changes. <br>
Risk: Persistent browser state, cookies, credentials, and logs can expose secrets. <br>
Mitigation: Use ephemeral sessions by default, treat saved state as sensitive, avoid persistent login state unless required, redact tokens in outputs, and rotate or delete state after use. <br>


## Reference(s): <br>
- [Agent Browser Core on ClawHub](https://clawhub.ai/codedao12/agent-browser-core) <br>
- [Agent Browser Overview](references/agent-browser-overview.md) <br>
- [Agent Browser Command Map](references/agent-browser-command-map.md) <br>
- [Safety and Risk Controls](references/agent-browser-safety.md) <br>
- [Agent Browser Workflows](references/agent-browser-workflows.md) <br>
- [Troubleshooting](references/agent-browser-troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guardrails for browser sessions, target allowlists, snapshots, refs, and high-risk command approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
