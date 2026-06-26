## Description: <br>
OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tang2606](https://clawhub.ai/user/tang2606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to plan deterministic web automation through the agent-browser CLI, including snapshot-driven navigation, command sequencing, and operational guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers high-privilege browser automation capabilities including arbitrary JavaScript execution, local file access, traffic manipulation, downloads, credential handling, and persistent browser state. <br>
Mitigation: Require explicit approval for sensitive capabilities, allowlist target domains, block localhost and private networks, keep sessions ephemeral by default, and redact secrets from logs and outputs. <br>
Risk: The skill depends on an external agent-browser CLI package and browser runtime. <br>
Mitigation: Verify the publisher and package before installation, pin a reviewed version, install browser dependencies in a dedicated low-privilege environment, and review upgrades before use. <br>


## Reference(s): <br>
- [Agent Browser Overview](references/agent-browser-overview.md) <br>
- [Agent Browser Command Map](references/agent-browser-command-map.md) <br>
- [Safety and Risk Controls](references/agent-browser-safety.md) <br>
- [Agent Browser Workflows](references/agent-browser-workflows.md) <br>
- [Troubleshooting](references/agent-browser-troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-output recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guardrails and approval requirements for sensitive browser automation actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
