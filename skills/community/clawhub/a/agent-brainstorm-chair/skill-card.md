## Description:

A structured multi-agent brainstorming facilitator that auto-detects Hermes/OpenClaw modes and guides two-phase debate, round control, role assignment, and baton handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usewild2026](https://clawhub.ai/user/usewild2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to chair structured brainstorming across one or more agents, separating strategy judgment from execution planning while enforcing round limits and handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenClaw bridge can expose more local computer authority than the skill's read-only brainstorming purpose needs.

Mitigation: Use only with a trusted local OpenClaw binary and trusted contacted agents; disable ACP filesystem-write and terminal capabilities where possible.

Risk: Meeting prompts or agent responses may expose sensitive context through local agent sessions or environment-backed workflows.

Mitigation: Run in a low-privilege or sandboxed environment and avoid placing secrets in environment variables or prompts.

Risk: Broad meeting phrases can trigger multi-agent consultation unexpectedly.

Mitigation: Use explicit invocation and confirm participant agent IDs and roles before using ACP mode.

## Reference(s):

- [Agent Brainstorm Chair ClawHub Listing](https://clawhub.ai/usewild2026/skills/agent-brainstorm-chair)
- [Adapter Guide](ADAPTERS.md)
- [Setup Guide](SETUP_GUIDE.md)
- [ClawHub Publishing Workflow](references/clawhub-publishing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown/text responses with optional JSON from helper scripts and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local OpenClaw ACP agents when available; otherwise runs as a simulated facilitator workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
