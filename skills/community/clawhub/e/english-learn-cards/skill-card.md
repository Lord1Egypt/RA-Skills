## Description:

Flashcard-based English vocabulary learning with SQLite and spaced repetition, usable with any chat platform when paired with an OpenClaw agent prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[racymind](https://clawhub.ai/user/racymind)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to maintain an English vocabulary flashcard database, render study cards, and run spaced-repetition reviews through a chat-agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional online pronunciation lookup can send a headword or phrase to Cambridge Dictionary, which may matter for privacy-sensitive vocabulary lists.

Mitigation: Remove --fill-audio from the prompt template or require explicit user consent before enabling online audio lookup.

Risk: The local SQLite vocabulary database can contain personal study history or sensitive terms.

Mitigation: Keep the database local, do not commit it, and set ENGLISH_LEARN_CARDS_DB to an appropriate private path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/racymind/skills/english-learn-cards)
- [Agent prompt template](artifact/prompt-examples/AGENT_PROMPT_TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and deterministic text output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database controlled by ENGLISH_LEARN_CARDS_DB; optional audio lookup can add pronunciation URLs.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
