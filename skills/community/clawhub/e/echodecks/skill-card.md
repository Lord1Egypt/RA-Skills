## Description:

EchoDecks lets agents manage flashcard decks, study reviews, AI-generated cards, and podcast summaries through the EchoDecks API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drgeld](https://clawhub.ai/user/drgeld)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to list EchoDecks decks and due cards, submit spaced repetition reviews, generate flashcards from topics or text, generate or retrieve podcasts, and inspect user study statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends deck data, prompts, raw text, study reviews, profile requests, and the API key to EchoDecks.

Mitigation: Install only if EchoDecks is trusted with that data and keep ECHODECKS_API_KEY in protected environment configuration.

Risk: Card and podcast generation actions may spend EchoDecks credits.

Mitigation: Review commands before running generation actions and confirm that the requested deck and content are intended.

Risk: Untrusted deck, card, or podcast IDs may be unsafe until the client uses structured URL parameter encoding.

Mitigation: Avoid passing untrusted IDs to the skill and prefer known EchoDecks identifiers from trusted account data.

## Reference(s):

- [EchoDecks ClawHub skill page](https://clawhub.ai/drgeld/skills/echodecks)
- [drgeld publisher profile](https://clawhub.ai/user/drgeld)
- [EchoDecks service](https://echodecks.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, JSON]

**Output Format:** [JSON responses and concise command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY; generation actions may spend EchoDecks credits.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
