## Description: <br>
Manage flashcards, generate AI-based cards, create audio podcasts, and track study progress using EchoDecks API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drgeld](https://clawhub.ai/user/drgeld) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Learners and agents use this skill to manage EchoDecks decks and cards, generate study flashcards and podcasts, retrieve study links, and submit spaced-repetition reviews through the EchoDecks API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Study material, deck metadata, review activity, and account profile information are sent to EchoDecks when the skill performs API-backed actions. <br>
Mitigation: Install only if EchoDecks is trusted for the requested study content, and avoid submitting secrets or regulated data. <br>
Risk: Generation actions can consume EchoDecks credits and create persistent content in the user's account. <br>
Mitigation: Confirm credit-consuming requests before generating flashcards or podcasts, and review created content in EchoDecks after use. <br>
Risk: The skill depends on the ECHODECKS_API_KEY environment variable for account access. <br>
Mitigation: Keep the API key private, provide it only through the environment, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drgeld/flashcards-podcasts-master) <br>
- [Publisher profile](https://clawhub.ai/user/drgeld) <br>
- [EchoDecks developer settings](https://echodecks.app/settings/developer) <br>
- [EchoDecks](https://echodecks.com) <br>
- [API_DOCS.md](artifact/API_DOCS.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call EchoDecks API actions that read or create account content, consume credits, and return persistent study resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
