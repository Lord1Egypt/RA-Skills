## Description:

Use when user asks about Agent architecture, design, or how an Agent works. Two-layer teaching: Layer 1 explains Agent concepts (agent loop, tool calling, memory, session, config), Layer 2 reads the Agent's own source code to explain specific architecture. Follows the Self-Explanation Protocol: always search code before answering architecture questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyxin-del](https://clawhub.ai/user/joeyxin-del)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users, learners, and developers use this skill to ask architecture questions and receive either plain-language Agent concepts or source-grounded explanations with file references for a specific Agent implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Layer 2 architecture questions can cause the agent to inspect local source code and quote file paths or line references.

Mitigation: Use this skill only in codebases where source-level disclosure to the requesting user is appropriate.

Risk: If source code is unavailable, architecture answers may become generic rather than implementation-specific.

Mitigation: Require the agent to state that source access is unavailable and avoid fabricated code references.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joeyxin-del/skills/agent-native-speaker)
- [Harness Engineering Glossary](references/harness-engineering-glossary.md)
- [Trigger Domain Reference](references/trigger-domain-reference.md)
- [Hermes Agent Architecture Map](references/hermes-agent-architecture-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with source file references and occasional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Layer 2 answers should cite local source paths and line references when source code is accessible.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
