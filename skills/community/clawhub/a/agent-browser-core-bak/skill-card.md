## Description:

OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tang2606](https://clawhub.ai/user/tang2606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to plan deterministic browser automation with the agent-browser CLI, including snapshot-based navigation, refs, JSON output, and operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can expose high-privilege capabilities such as arbitrary JavaScript execution, local file access, traffic manipulation, persistent state, cookies, and credentials.

Mitigation: Require explicit approval for eval, file access, proxies, network interception, credentials, and persistent state reuse; allowlist target domains and treat profiles, saved state, cookies, and credentials as secrets.

Risk: Unpinned CLI or browser-runtime installation can introduce package-resolution and upgrade risk.

Mitigation: Pin the exact agent-browser version, review upgrades, prefer a container or dedicated environment, and avoid the unpinned npx Playwright dependency fallback unless that risk is accepted.

## Reference(s):

- [Agent Browser Overview](artifact/references/agent-browser-overview.md)
- [Agent Browser Command Map](artifact/references/agent-browser-command-map.md)
- [Safety and Risk Controls](artifact/references/agent-browser-safety.md)
- [Agent Browser Workflows](artifact/references/agent-browser-workflows.md)
- [Troubleshooting](artifact/references/agent-browser-troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON-mode browser snapshots and command sequences for agent execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
