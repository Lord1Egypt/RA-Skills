## Description: <br>
Daily self-improving questionnaire that learns about the user and refines agent behavior by asking one Telegram question at a time and updating USER.md and SOUL.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daijo-bu](https://clawhub.ai/user/daijo-bu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users who want recurring personalization can use this skill to ask daily Telegram questions about personal preferences and desired agent behavior, then fold answers into USER.md and SOUL.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questionnaire answers may persist sensitive personal preferences or behavior guidance in USER.md and SOUL.md. <br>
Mitigation: Avoid sharing secrets in answers, review USER.md and SOUL.md periodically, and disable the routine if recurring profile updates are not desired. <br>
Risk: Recurring Telegram prompts can influence future agent behavior through stored profile updates. <br>
Mitigation: Keep questions limited, inspect updates after each round, and remove any profile details that should not guide future agent responses. <br>


## Reference(s): <br>
- [Daily Questions release page](https://clawhub.ai/daijo-bu/daily-questions) <br>
- [example-questions.md](references/example-questions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Tool calls] <br>
**Output Format:** [Markdown instructions with Telegram message payload examples and local profile file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one-at-a-time questionnaire prompts, multiple choice options, Telegram inline button payloads, and updates to USER.md and SOUL.md.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
