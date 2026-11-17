## Description:

AI-powered flashcard management with automated podcast generation and spaced-repetition study tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drgeld](https://clawhub.ai/user/drgeld)

### License/Terms of Use:


## Use Case:

External users and learners use this skill to let an agent manage EchoDecks flashcards, quiz due cards, submit spaced-repetition reviews, generate new cards from topics or text, and create study podcasts from deck content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the EchoDecks API key, deck and card content, submitted text, review activity, podcast requests, and account metadata to a configured remote API.

Mitigation: Install only if the EchoDecks provider is trusted, review the data being sent, and use a revocable, least-privilege API key if EchoDecks supports one.

Risk: The configured API host is a hardcoded echodecks.com endpoint while the documented key source is echodecks.app.

Mitigation: Confirm that echodecks.com is an official EchoDecks API host for keys obtained from echodecks.app before use.

Risk: Card and podcast generation can consume EchoDecks credits.

Mitigation: Confirm deck IDs and generation requests before running card or podcast generation actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drgeld/skills/echodecks-ultimate)
- [drgeld publisher profile](https://clawhub.ai/user/drgeld)
- [EchoDecks](https://echodecks.app)
- [EchoDecks settings](https://echodecks.app/settings)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON returned from EchoDecks API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY and can trigger remote EchoDecks API calls that create decks, generate cards, submit reviews, retrieve user stats, and generate podcasts.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
