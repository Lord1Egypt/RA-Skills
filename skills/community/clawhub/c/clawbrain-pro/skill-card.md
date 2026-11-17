## Description:

ClawBrain Pro adds ClawBrain model routing, persistent memory, recall, diagnostics, benchmarking, smart retry, and output verification guidance for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfeng](https://clawhub.ai/user/michaelfeng)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to configure ClawBrain-backed model routing and memory features, and to invoke diagnostics, recall, retry guidance, and benchmarks for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, possible memory content, and diagnostic metadata may be sent to the third-party ClawBrain or factorhub service.

Mitigation: Use a scoped API key, avoid sensitive conversations unless retention controls are clear, and review the provider's handling of stored memory and diagnostics before deployment.

Risk: Benchmark, doctor, and retry flows can guide shell command use, dependency installation, and broad automation.

Mitigation: Require review of exact commands and dependency changes before execution, especially in production or privileged environments.

Risk: Persistent memory can retain user, project, preference, and decision information across sessions.

Mitigation: Avoid storing secrets or regulated data in memory and periodically review, correct, or delete retained memory records.

Risk: The authoritative security verdict is suspicious because the release combines third-party model and memory services with broad automation and limited consent scoping evidence.

Mitigation: Pilot in a sandboxed workspace, restrict credentials and tool permissions, and approve use only after organizational review of data exposure and automation controls.

## Reference(s):

- [ClawBrain Pro ClawHub listing](https://clawhub.ai/michaelfeng/skills/clawbrain-pro)
- [ClawBrain homepage from ClawHub metadata](https://github.com/michaelfeng/clawbrain)
- [ClawBrain dashboard](https://clawbrain.dev/dashboard)
- [OpenClaw model comparison report](https://clawbrain.dev/blog/openclaw-model-comparison)
- [ClawBrain service homepage](https://clawbrain.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use third-party ClawBrain or factorhub services when configured by the user.]

## Skill Version(s):

1.6.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
