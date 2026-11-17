## Description:

OpenClaw skill for the agent-browser CLI (Rust-based with Node.js fallback) enabling AI-friendly web automation with snapshots, refs, and structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lion504](https://clawhub.ai/user/lion504)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and operate deterministic browser automation through the agent-browser CLI, including snapshot-first navigation, ref-based actions, JSON-oriented workflows, and safety guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can expose credentials, cookies, saved sessions, or browser state.

Mitigation: Treat browser state as secret, use ephemeral sessions where possible, redact tokens from outputs, and isolate the environment.

Risk: High-risk browser controls such as eval, local file access, custom browser arguments, proxies, or traffic interception can expand the skill's impact.

Mitigation: Require explicit approval before enabling those controls, pin the agent-browser version, and run the CLI without elevated OS privileges.

## Reference(s):

- [Agent Browser Overview](references/agent-browser-overview.md)
- [Agent Browser Command Map](references/agent-browser-command-map.md)
- [Safety and Risk Controls](references/agent-browser-safety.md)
- [Agent Browser Workflows](references/agent-browser-workflows.md)
- [Troubleshooting](references/agent-browser-troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/lion504/skills/agent-browser-core-1-0-1)
- [Publisher Profile](https://clawhub.ai/user/lion504)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces command sequences, workflow guidance, and operational guardrails for browser automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
