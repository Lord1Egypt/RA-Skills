## Description:

Batch add word cards to Anki via AnkiConnect. Supports Spanish-Chinese vocabulary cards with automatic translation and example sentences. Use when the user wants to add multiple words to Anki at once, import vocabulary lists, or bulk-create flashcards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fondas123](https://clawhub.ai/user/fondas123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and language learners use this skill to turn word lists into Anki vocabulary cards in bulk, including Spanish-Chinese cards with meanings and example sentences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can add cards to the user's local Anki collection.

Mitigation: Use the dry-run option before large imports and confirm the target deck and model before writing cards.

Risk: AnkiConnect exposes local control over Anki through an HTTP endpoint.

Mitigation: Keep AnkiConnect limited to local access and avoid exposing the local endpoint to untrusted networks.

## Reference(s):

- [AnkiConnect](https://foosoft.net/projects/anki-connect/)
- [ClawHub skill page](https://clawhub.ai/fondas123/skills/anki-batch-cards)
- [Publisher profile](https://clawhub.ai/user/fondas123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TSV or JSON card data and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local AnkiConnect endpoint and can use dry-run output before adding cards.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
