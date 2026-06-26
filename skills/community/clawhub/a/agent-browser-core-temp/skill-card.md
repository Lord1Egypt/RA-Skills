## Description: <br>
OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmyg11](https://clawhub.ai/user/mmyg11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan deterministic browser automation with the agent-browser CLI, including snapshot-first navigation, ref-based actions, JSON output, and operational guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can access authenticated sessions, credentials, cookies, storage, local files, network controls, proxies, CDP, downloads, or arbitrary JavaScript when sensitive controls are enabled. <br>
Mitigation: Use a dedicated environment, allowlist target domains, keep sessions ephemeral, protect saved state, avoid eval/file access/proxy/CDP/cookie or storage mutation unless explicitly approved, and redact tokens in logs and outputs. <br>
Risk: The server security summary notes a minor identity/version mismatch. <br>
Mitigation: Verify the ClawHub skill identity, publisher handle, agent-browser package owner, and intended package version before relying on the skill. <br>


## Reference(s): <br>
- [Agent Browser Core Temp on ClawHub](https://clawhub.ai/mmyg11/agent-browser-core-temp) <br>
- [Agent Browser Overview](references/agent-browser-overview.md) <br>
- [Agent Browser Command Map](references/agent-browser-command-map.md) <br>
- [Safety and Risk Controls](references/agent-browser-safety.md) <br>
- [Agent Browser Workflows](references/agent-browser-workflows.md) <br>
- [Troubleshooting](references/agent-browser-troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes JSON-mode automation, safe defaults, allowlisted domains, and explicit approval for sensitive browser controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
