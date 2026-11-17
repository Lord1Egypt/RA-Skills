## Description:

OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tang2606](https://clawhub.ai/user/tang2606)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan deterministic browser automation workflows with the agent-browser CLI, including snapshots, ref-based actions, JSON output, and operational guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can expose credentials, session state, local files, downloads, or network traffic when high-risk commands are enabled.

Mitigation: Use domain allowlists, ephemeral sessions, redacted logs, and explicit human approval before credentials, storage, downloads, local file access, eval, proxying, or network interception.

Risk: Unpinned setup commands can introduce supply-chain uncertainty.

Mitigation: Pin exact package versions and install in a dedicated environment or through a lockfile-controlled local Playwright runtime.

Risk: Running the browser automation CLI with elevated privileges increases impact if a page or command is unsafe.

Mitigation: Run without elevated OS privileges and prefer isolated environments or containers.

## Reference(s):

- [Agent Browser Overview](references/agent-browser-overview.md)
- [Agent Browser Command Map](references/agent-browser-command-map.md)
- [Safety and Risk Controls](references/agent-browser-safety.md)
- [Agent Browser Workflows](references/agent-browser-workflows.md)
- [Troubleshooting](references/agent-browser-troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command sequences and guardrails; does not run browser automation itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
