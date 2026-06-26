## Description: <br>
Manage, create, and study flashcards, generate AI-based cards and podcasts, and track progress using EchoDecks API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drgeld](https://clawhub.ai/user/drgeld) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and learning-focused agents use this skill to manage EchoDecks flashcard decks, generate study cards and audio podcasts, retrieve study links, and submit spaced-repetition reviews through the EchoDecks API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a broad EchoDecks API key that can access account data and perform account actions. <br>
Mitigation: Use only an API key approved for the intended account scope, store it in ECHODECKS_API_KEY, and rotate or revoke it if access is no longer needed. <br>
Risk: Generation, podcast creation, and review submission can consume credits or change account history. <br>
Mitigation: Require explicit user confirmation before card generation, podcast creation, or review submission. <br>
Risk: Study material submitted to EchoDecks may include confidential or regulated content. <br>
Mitigation: Avoid submitting confidential or regulated study material unless EchoDecks is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drgeld/echodecks-clawdbot-skill) <br>
- [EchoDecks Developer Settings](https://echodecks.app/settings/developer) <br>
- [EchoDecks website](https://echodecks.com) <br>
- [API documentation](API_DOCS.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY; API actions may create or modify account content and consume EchoDecks credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
