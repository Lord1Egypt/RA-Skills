## Description: <br>
OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tang2606](https://clawhub.ai/user/tang2606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan controlled browser automation with the agent-browser CLI, including snapshot-first navigation, ref-based actions, JSON-friendly command output, and operational guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can interact with live sites, private networks, or sensitive pages beyond the intended task. <br>
Mitigation: Use domain allowlists, block localhost and private-network targets by default, and require explicit approval before high-risk actions. <br>
Risk: The external agent-browser package and browser runtime add supply-chain and execution-environment risk. <br>
Mitigation: Verify and pin the trusted package version, install in a dedicated profile or container, and avoid elevated OS privileges. <br>
Risk: Credentials, cookies, storage files, downloads, proxies, local file access, and eval can expose secrets or change system state. <br>
Mitigation: Keep sessions ephemeral, treat state files as secrets, redact tokens, and require approval before credential, storage, download, network-routing, local-file, or eval operations. <br>


## Reference(s): <br>
- [Agent Browser Overview](references/agent-browser-overview.md) <br>
- [Agent Browser Command Map](references/agent-browser-command-map.md) <br>
- [Safety and Risk Controls](references/agent-browser-safety.md) <br>
- [Agent Browser Workflows](references/agent-browser-workflows.md) <br>
- [Troubleshooting](references/agent-browser-troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and structured operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command sequences and guardrails for an agent; no executable files are included.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
