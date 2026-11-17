## Description:

Builds an installable personality skill that models a named person's communication style, judgment patterns, and audience-aware behavior from authorized connected communication samples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create or refresh a named person's personality skill from communication sources they are already authorized to access. The generated skill helps an agent respond in that person's voice and decision style, while the user remains responsible for consent, source selection, and deployment controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can profile and persistently impersonate real people using sensitive communications.

Mitigation: Install and run it only with clear authorization, target-person consent, and explicit disclosure when a real-person persona is active.

Risk: Broad email, chat, transcript, or document connector access may expose more communication data than intended.

Mitigation: Review available MCP connectors and scopes before use, choose specific sources deliberately, and avoid broad defaults unless the user explicitly intends them.

Risk: A generated persona can be mistaken for factual memory or a fully faithful digital twin.

Mitigation: Treat the output as a personality, voice, and judgment profile only; use separate reviewed memory systems for factual recall when needed.

## Reference(s):

- [Personality Skill Template](artifact/references/personality_skill_template.md)
- [Pillar 1: Linguistic Profiling](artifact/references/pillar_1_linguistic.md)
- [Pillar 2: Psychometric Profiling](artifact/references/pillar_2_psychometric.md)
- [Pillar 3: Judgment & Decision Pattern Profiling](artifact/references/pillar_3_judgment.md)
- [Pillar 4: Contextual Audience Profiling](artifact/references/pillar_4_audience.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown skill files and structured profile documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an installable personality skill directory with SKILL.md and profile reference files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
