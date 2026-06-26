## Description: <br>
AI-powered flashcard management with automated podcast generation and spaced-repetition study tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drgeld](https://clawhub.ai/user/drgeld) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External learners and study-focused agents use this skill to manage EchoDecks flashcards, review due cards with spaced repetition, generate cards from topics or text, and create podcast summaries from study decks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EchoDecks API key. <br>
Mitigation: Treat ECHODECKS_API_KEY as a secret and provide it only in trusted agent environments. <br>
Risk: Study material and account actions are sent to EchoDecks. <br>
Mitigation: Install and use the skill only when EchoDecks is trusted with the study content and requested account actions. <br>
Risk: Card and podcast generation can consume EchoDecks credits. <br>
Mitigation: Confirm before running generation actions, especially podcast generation or bulk card creation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drgeld/echodecks-ultimate) <br>
- [EchoDecks](https://echodecks.app) <br>
- [EchoDecks Settings](https://echodecks.app/settings) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses with concise text guidance and command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY; card and podcast generation actions may consume EchoDecks credits.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
