## Description: <br>
Flashcard-based English vocabulary learning with SQLite + SRS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RacyMind](https://clawhub.ai/user/RacyMind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage English vocabulary flashcards, run spaced-repetition reviews, and render concise study cards through a local SQLite-backed helper CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper writes a local SQLite vocabulary database under the configured path. <br>
Mitigation: Set ENGLISH_LEARN_CARDS_DB deliberately and avoid committing the database or other local-only files. <br>
Risk: Optional audio lookup can send headwords or phrases to Cambridge Dictionary. <br>
Mitigation: Avoid --fill-audio and --audio-auto for sensitive phrases unless that external lookup is acceptable. <br>


## Reference(s): <br>
- [Agent Prompt Template](artifact/prompt-examples/AGENT_PROMPT_TEMPLATE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/RacyMind/english-learn-cards) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper stores vocabulary and review state in a local SQLite database configured by ENGLISH_LEARN_CARDS_DB.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
