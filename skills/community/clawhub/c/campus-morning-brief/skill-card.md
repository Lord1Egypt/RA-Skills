## Description:

Creates a concise, age-appropriate, personalized daily campus morning brief with local weather, verified current news, a bilingual quote, study guidance, reminders, and a concrete action prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[my12121-beep](https://clawhub.ai/user/my12121-beep)

### License/Terms of Use:

MIT

## Use Case:

External developers, educators, parents, and student-assistant agents use this skill to create short, source-backed morning briefs for students, classes, or family routines. It helps agents gather current weather and news, apply age-appropriate editorial guidance, validate a structured brief payload, and render shareable local outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live weather and news may be stale, inaccurate, or inappropriate for a student audience.

Mitigation: Fetch current sources, prefer authoritative publishers, preserve direct URLs and publication dates, filter age-inappropriate material, and review generated links before sharing.

Risk: Student profile data or generated briefs could expose sensitive personal information.

Mitigation: Use minimal profile data and avoid sensitive schedules, health details, identifiers, contact information, credentials, and delivery identifiers.

Risk: Automated posting, printing, or sending could distribute a brief before review.

Mitigation: Keep delivery separate from generation and require explicit authorization unless an established automation already grants it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/my12121-beep/skills/campus-morning-brief)
- [Brief schema](references/brief.schema.json)
- [Configuration example](references/config.example.json)
- [Content guidelines](references/content-guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON payloads, JSON metadata, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated briefs include source links and dates; local rendering writes morning-brief.md, morning-brief.html, and metadata.json.]

## Skill Version(s):

1.0.3 (source: server release evidence, README.md, PROMOTION.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
