## Description:

Big8 is a Chinese metaphysics and fortune-telling assistant for BaZi charts, face reading, feng shui photo review, horoscopes, I Ching divination, and daily almanac guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Big8 as an entertainment-oriented Chinese metaphysics assistant to generate BaZi readings, feng shui layout suggestions, face-reading commentary, horoscope or zodiac guidance, I Ching-style divination, and daily almanac notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive birth dates, selfies, and room photos.

Mitigation: Use only necessary personal inputs, avoid uploading other people's photos, and rely on the stated discard-after-analysis behavior.

Risk: Fortune-telling, feng shui, face-reading, and horoscope outputs may be mistaken for life, medical, legal, or financial advice.

Mitigation: Treat outputs as entertainment and do not use them as the basis for medical, legal, financial, or major life decisions.

Risk: Running Python helper commands may require installing dependencies.

Mitigation: Install dependencies in a pinned virtual environment before running helper scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kobenfang/skills/big8)
- [Skill instructions](artifact/SKILL.md)
- [Big8 product plan](artifact/big8-plan.md)
- [BaZi knowledge reference](artifact/scripts/knowledge/bazi.yaml)
- [Feng shui knowledge reference](artifact/scripts/knowledge/fengshui.yaml)
- [Face-reading knowledge reference](artifact/scripts/knowledge/face.yaml)
- [Zodiac knowledge reference](artifact/scripts/knowledge/zodiac.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style Chinese responses with occasional JSON from local helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Entertainment guidance only; photo and birth-date inputs may be sensitive.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
