## Description:

Helps agents write, deliver, lint, and diagnose concise, natural IM or DM messages while adapting to the active persona, with voice notes available only by opt-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nb-corp](https://clawhub.ai/user/nb-corp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal-agent builders use this skill to draft concise chat replies for bubble-tool and plain-reply surfaces, adapt tone to persona and context, lint messages, and configure proactive outreach or opt-in voice notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a high-confidence instruction-priority weakness that may create unsafe instruction ordering.

Mitigation: Before installing, ask whether the instruction ordering concern has been corrected and clarify the skill's required file access and the permissions enforced by the host.

Risk: The security analysis is incomplete because several local references could not be resolved.

Mitigation: Review the unresolved references and reassess the skill before installation.

## Reference(s):

- [Chat Human on ClawHub](https://clawhub.ai/nb-corp/skills/chat-human)
- [Project homepage](https://github.com/NB-Corp/chat-human)
- [Bubble and voice patterns](references/bubble-and-voice-patterns.md)
- [Persona and mood physics](references/persona-and-mood-physics.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Short chat text, structured message payloads, and optional code or table artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mobile-friendly concise beats; voice notes are opt-in.]

## Skill Version(s):

0.2.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
