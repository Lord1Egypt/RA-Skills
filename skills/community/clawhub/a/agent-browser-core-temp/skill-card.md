## Description:

OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmyg11](https://clawhub.ai/user/mmyg11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan deterministic browser automation with the agent-browser CLI, including snapshot-driven navigation, structured command output, and operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional unpinned Playwright installation can introduce supply-chain drift.

Mitigation: Pin the agent-browser version and prefer lockfile-controlled or pinned Playwright installation.

Risk: Browser automation can expose secrets or local resources when credential, cookie, storage, proxy, file-access, eval, or custom-runtime features are enabled.

Mitigation: Run browser tooling in a dedicated low-privilege environment and require explicit approval before using those capabilities.

## Reference(s):

- [Agent Browser Overview](references/agent-browser-overview.md)
- [Agent Browser Command Map](references/agent-browser-command-map.md)
- [Safety and Risk Controls](references/agent-browser-safety.md)
- [Agent Browser Workflows](references/agent-browser-workflows.md)
- [Troubleshooting](references/agent-browser-troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline CLI commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-mode command recommendations for machine parsing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
