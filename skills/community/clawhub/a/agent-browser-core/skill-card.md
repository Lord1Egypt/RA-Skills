## Description:

OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codedao12](https://clawhub.ai/user/codedao12)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to plan browser automation with the agent-browser CLI, including snapshot-first navigation, ref-based actions, JSON outputs, and safe operating guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can access authenticated sessions, credentials, cookies, storage, and other sensitive state.

Mitigation: Use ephemeral sessions where possible, treat state files as secrets, redact tokens from logs, and require explicit approval before credential or state mutation.

Risk: High-risk browser controls can execute arbitrary JavaScript, access local files, change runtime behavior, or intercept traffic.

Mitigation: Disallow eval, local file access, custom runtime flags, proxies, and traffic interception by default; use domain allowlists and block localhost or private network targets.

Risk: Installing and running the browser CLI can introduce supply-chain or host-environment risk.

Mitigation: Install in a dedicated non-root environment, pin exact trusted versions of agent-browser and Playwright, and avoid global installs where possible.

## Reference(s):

- [Agent Browser Overview](references/agent-browser-overview.md)
- [Agent Browser Command Map](references/agent-browser-command-map.md)
- [Safety and Risk Controls](references/agent-browser-safety.md)
- [Agent Browser Workflows](references/agent-browser-workflows.md)
- [Troubleshooting](references/agent-browser-troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command sequences and operational guardrails for browser automation workflows.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
