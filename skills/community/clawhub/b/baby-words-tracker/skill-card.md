## Description:

Records and tracks a baby's spoken words and phrases, supports multiple languages and partial-word bracket notation, classifies vocabulary by length, syncs records to Feishu documents, and generates language development reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suiclaw](https://clawhub.ai/user/suiclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this skill to record a child's emerging vocabulary, classify words across Mandarin, Cantonese, English, and other languages, avoid duplicate entries, and view concise vocabulary growth summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records a child's speech history and may sync that sensitive data to Feishu.

Mitigation: Use only when the caregiver accepts that storage and sync behavior, confirm retention and deletion expectations, and keep records local-only when cloud sync is not needed.

Risk: The artifact README recommends placing a Feishu document token in SKILL.md.

Mitigation: Store Feishu credentials through a protected secret mechanism, limit token permissions, and avoid committing real tokens to skill files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suiclaw/skills/baby-words-tracker)
- [Publisher profile](https://clawhub.ai/user/suiclaw)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with vocabulary summaries and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local JSON database and sync vocabulary records to Feishu when configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
