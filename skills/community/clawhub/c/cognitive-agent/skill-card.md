## Description:

Cognitive Agent is a framework-style skill for designing AI agents with long-term memory, spaced-repetition learning, emotional context, and metacognitive reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1580021414-afk](https://clawhub.ai/user/1580021414-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to prototype assistants that remember user preferences and interaction history, support adaptive learning or knowledge management, and generate memory, study-plan, emotional-response, and reflection patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage agents to retain long-term local memory about users, preferences, interaction history, emotions, and logs without clear privacy controls.

Mitigation: Require explicit opt-in before collecting memory, provide inspect/export/delete controls, set retention limits, and redact sensitive content from logs and memories.

Risk: The uploaded artifact declares runtime entry points and ranged dependencies, but the server security guidance calls for verifying the missing runtime implementation and pinning dependencies.

Mitigation: Review the complete runtime implementation before deployment, pin dependency versions, and run security scans on the resolved dependency tree.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1580021414-afk/skills/cognitive-agent)
- [Skill source documentation](artifact/SKILL.md)
- [Quick start guide](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, JSON, JavaScript, TypeScript, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe memory records, learning plans, emotional-state records, API shapes, and reflection reports.]

## Skill Version(s):

1.0.0 (source: server release evidence, OpenClaw metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
