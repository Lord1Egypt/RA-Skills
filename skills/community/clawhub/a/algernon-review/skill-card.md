## Description: <br>
Runs FSRS-4.5 review sessions for OpenAlgernon cards, including binary flashcards, AI-evaluated open-ended answers, automatic scheduling, promotions, correction cards, and session logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntonioVFranco](https://clawhub.ai/user/AntonioVFranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenAlgernon users use this skill to review due study cards, receive feedback on free-text answers, and update their local spaced-repetition schedule. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill updates the local OpenAlgernon study database and appends review activity to local session logs. <br>
Mitigation: Back up or periodically clean ~/.openalgernon data when study topics are sensitive, and run the skill only where local database changes are expected. <br>
Risk: Generated correction or promotion cards may preserve inaccurate feedback from an open-ended review. <br>
Mitigation: Review generated correction and promotion cards before relying on them in future study sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AntonioVFranco/algernon-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown conversation output with inline SQLite and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local OpenAlgernon SQLite study data and append local session logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
