## Description: <br>
OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lion504](https://clawhub.ai/user/Lion504) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and operate agent-browser CLI workflows for deterministic browser automation, including navigation, snapshots, element refs, and structured command output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can interact with unintended sites or internal network resources. <br>
Mitigation: Allowlist intended target domains and block localhost and private network targets before opening URLs. <br>
Risk: High-privilege browser controls can execute JavaScript, access local files, manipulate traffic, or use custom runtimes. <br>
Mitigation: Require explicit human approval before using eval, file access, downloads, proxy or network interception, custom executable paths, custom browser args, or CDP controls. <br>
Risk: Credentials, cookies, storage, and saved session state can expose secrets. <br>
Mitigation: Use ephemeral or dedicated sessions by default, treat state files as secrets, redact tokens from logs, and approve credential or storage changes only when required. <br>
Risk: Unpinned or untrusted CLI installation can introduce supply-chain exposure. <br>
Mitigation: Verify and pin the trusted agent-browser package version, install in a dedicated or containerized environment, and avoid elevated OS privileges. <br>


## Reference(s): <br>
- [Agent Browser Core ClawHub Page](https://clawhub.ai/Lion504/agent-browser-core-1-0-1) <br>
- [Agent Browser Overview](references/agent-browser-overview.md) <br>
- [Agent Browser Command Map](references/agent-browser-command-map.md) <br>
- [Agent Browser Safety](references/agent-browser-safety.md) <br>
- [Agent Browser Workflows](references/agent-browser-workflows.md) <br>
- [Agent Browser Troubleshooting](references/agent-browser-troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON command output, snapshots, refs, waits, and operational guardrails for browser automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json version is 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
