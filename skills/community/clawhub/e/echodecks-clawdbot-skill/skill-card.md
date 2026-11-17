## Description:

Manage, create, and study flashcards, generate AI-based cards and podcasts, and track progress using EchoDecks API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drgeld](https://clawhub.ai/user/drgeld)

### License/Terms of Use:


## Use Case:

Learners and agents connected to an EchoDecks account use this skill to manage decks and cards, generate study material and podcasts, open study sessions, and submit spaced-repetition reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ECHODECKS_API_KEY to access and modify an EchoDecks account.

Mitigation: Treat the API key like a password and install only when the agent should use that account.

Risk: Generation, podcast, deck creation, and review commands can spend credits or change account state.

Mitigation: Confirm credit-spending or state-changing commands before execution.

Risk: Study text and deck content may be sent to EchoDecks for AI card or podcast generation.

Mitigation: Avoid sending sensitive material unless sharing it with EchoDecks is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drgeld/skills/echodecks-clawdbot-skill)
- [EchoDecks External API Documentation](artifact/API_DOCS.md)
- [EchoDecks README](artifact/README.md)
- [EchoDecks Developer Settings](https://echodecks.app/settings/developer)
- [EchoDecks](https://echodecks.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY; some commands can spend EchoDecks credits or change account state.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
