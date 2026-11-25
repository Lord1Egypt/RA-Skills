## Description:

Prepare a compact, durable handoff between OpenClaw sessions or agents without copying the full conversation. Use /compact for same-session context reduction; use this skill when work must continue in a fresh session or another runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theangrypit](https://clawhub.ai/user/theangrypit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare a concise, durable Markdown handoff for continuing work in a fresh OpenClaw session or another runtime. It preserves goals, decisions, evidence, and protected state; Codex history recall is an optional bounded workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reported no direct findings, but inspection was partial for some components, including executable scripts, so some behavior remains uncertain.

Mitigation: Review the partially inspected scripts and skill behavior before installation or execution.

## Reference(s):

- [OpenClaw session commands](https://docs.openclaw.ai/tools/slash-commands)
- [OpenClaw session management](https://docs.openclaw.ai/session)
- [OpenClaw continuity packet template](references/packet-template.md)
- [Optional legacy Codex workflow](references/codex-legacy-workflow.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Markdown continuity packet and JSON recall or acceptance evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a packet to a verified project workspace; optional legacy history recall is bounded and read-only.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
