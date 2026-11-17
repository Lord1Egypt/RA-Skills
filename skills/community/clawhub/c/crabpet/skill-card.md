## Description:

AI pet companion that turns OpenClaw usage into a pixel pet experience with status, personality, mood, achievements, summaries, and shareable pet cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liqiwa](https://clawhub.ai/user/liqiwa)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users use CrabPet to view and update a virtual pixel pet whose level, mood, personality, and achievements are derived from their local OpenClaw activity logs. The skill can generate text, Markdown, and optional PNG pet cards for sharing pet status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans local OpenClaw memory logs to infer activity, mood, and personality traits, then stores derived pet state locally.

Mitigation: Install only if local memory-log scanning is acceptable, and review generated pet cards before sharing because they may reveal usage patterns.

Risk: The security guidance flags an unsafe web/Chrome PNG rendering path for card generation.

Mitigation: Disable or fix the web/Chrome renderer before using PNG card generation, or use text and Markdown card output until the renderer is reviewed.

Risk: Untrusted or markup-like pet names may be embedded in generated cards.

Mitigation: Use plain pet names and sanitize or reject markup-like input before rendering shareable cards.

## Reference(s):

- [CrabPet README](README.md)
- [CrabPet Personality System](references/personality.md)
- [OpenClaw AI Pet Design](openclaw-ai-pet-design.md)
- [CrabPet ClawHub Skill Page](https://clawhub.ai/liqiwa/skills/crabpet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with JSON command output and generated text, Markdown, or PNG card files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional Pillow and Chrome/Chromium affect PNG card generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
