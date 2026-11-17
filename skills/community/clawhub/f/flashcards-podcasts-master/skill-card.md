## Description:

Manage flashcards, generate AI-based cards, create audio podcasts, and track study progress using EchoDecks API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drgeld](https://clawhub.ai/user/drgeld)

### License/Terms of Use:


## Use Case:

Learners and agents use this skill to manage EchoDecks flashcard decks, generate study cards and audio podcasts, retrieve study links, and submit spaced-repetition reviews through the EchoDecks API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an EchoDecks API key for authenticated API access.

Mitigation: Keep ECHODECKS_API_KEY private and provide it only in trusted execution environments.

Risk: Provided text, deck data, card data, review events, and podcast requests may be sent to EchoDecks.

Mitigation: Avoid submitting sensitive study material unless sharing it with EchoDecks is acceptable.

Risk: Flashcard and podcast generation commands can spend account credits.

Mitigation: Confirm the target deck, requested generation type, and expected credit cost before running generation commands.

Risk: Deck, card, and podcast identifiers supplied from untrusted sources may be used in API requests.

Mitigation: Use trusted identifiers and validate them before invoking deck, card, podcast, or study-session operations.

## Reference(s):

- [EchoDecks API Documentation](artifact/API_DOCS.md)
- [EchoDecks Developer Settings](https://echodecks.app/settings/developer)
- [EchoDecks](https://echodecks.com)
- [ClawHub Skill Page](https://clawhub.ai/drgeld/skills/flashcards-podcasts-master)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY; card and podcast generation actions can consume EchoDecks account credits.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
