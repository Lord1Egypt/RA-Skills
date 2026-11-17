## Description:

AGI数字伙伴 is a digital companion skill that uses a dual-cycle cognitive framework with intentionality analysis, personality mapping, metacognition checks, and an error-wisdom store to support dialogue, personalization, complex problem solving, and learning from mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a configurable AI companion for dialogue, reasoning, personality customization, memory-assisted responses, metacognitive review, and error-learning workflows. It is also useful for inspecting or extending a local Python cognitive-architecture toolkit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate as a local system tool with broad filesystem, process, environment, and shell-command capabilities.

Mitigation: Run it only in a disposable or sandboxed workspace with strict path limits, command allowlists, and explicit approval for destructive or sensitive actions.

Risk: Broad trigger conditions may cause system-tool behavior to be considered during ordinary user interactions.

Mitigation: Require clear user intent before invoking local tools, and review planned filesystem, process, environment, or shell operations before execution.

Risk: Local memory and personality files may persist user-provided information across sessions.

Mitigation: Use a dedicated memory directory, avoid storing secrets or sensitive personal data, and periodically review or clear persisted files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiwifruit13/skills/agi-evolution-model)
- [Architecture](references/architecture.md)
- [Behavior baseline](references/behavior-baseline.md)
- [Perception interface](references/perception-node.md)
- [Metacognition](references/metacognition.md)
- [Error wisdom](references/error-wisdom.md)
- [Usage examples](references/usage-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local memory and personality files under the configured memory directory when its scripts are used.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
