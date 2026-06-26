## Description: <br>
Interact with Anki flashcard decks via the AnkiConnect REST API. Use when the user wants to create, update, search, or manage Anki cards, decks, notes, or models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyroninja](https://clawhub.ai/user/gyroninja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent interact with a local Anki installation through AnkiConnect for creating, updating, searching, and managing flashcard decks, notes, cards, and models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent actions can modify local Anki decks, notes, cards, or models, including bulk changes. <br>
Mitigation: Review proposed Anki changes before allowing them, especially bulk edits. <br>
Risk: The skill depends on a locally running Anki installation with AnkiConnect installed. <br>
Mitigation: Install AnkiConnect from a trusted source and use this skill only when local Anki access is intended. <br>


## Reference(s): <br>
- [AnkiConnect Project](https://foosoft.net/projects/anki-connect/) <br>
- [AnkiConnect README](https://git.sr.ht/~foosoft/anki-connect/blob/master/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API calls] <br>
**Output Format:** [Markdown or plain text with AnkiConnect REST API request details as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Anki running with the AnkiConnect plugin installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
