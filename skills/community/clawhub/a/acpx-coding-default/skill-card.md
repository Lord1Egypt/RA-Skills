## Description:

Use direct acpx CLI via exec as the default coding execution path for Codex- and Claude-focused agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to route coding, debugging, refactoring, test-running, and repository tasks through the local acpx CLI while preserving explicit command visibility and fallback behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coding requests routed through the local acpx CLI may edit files or run project tooling.

Mitigation: Review prompts, commands, and repository context before use, especially in sensitive repositories.

Risk: The configured acpx binary, adapter, or toolchain may be missing or incompatible.

Mitigation: Check the plugin-local binary first and report the exact missing command or failure before using any fallback path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/acpx-coding-default)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Direct acpx CLI invocation templates for Codex and Claude adapters, including named-session and failure-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
