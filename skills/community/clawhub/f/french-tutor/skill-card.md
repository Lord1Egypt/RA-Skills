## Description:

French Tutor helps learners build practical French skills from A1 to C2 through interactive lessons, placement tests, roleplay, corrections, and Madame Dubois's humorous coaching persona.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharoonsharif](https://clawhub.ai/user/sharoonsharif)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use this skill to practice French through level-aware tutoring, placement assessment, vocabulary and grammar exercises, roleplay, pronunciation guidance, and corrective feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update french-tutor-progress.json with learning level, vocabulary, weak areas, and recent session history.

Mitigation: Run the skill in a workspace where that local progress file is acceptable, and delete french-tutor-progress.json when you do not want the record retained.

Risk: Humorous critique and language corrections may not match every learner's comfort level or may contain mistakes.

Mitigation: Review important translations before relying on them and ask the agent for gentler feedback or clarification when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sharoonsharif/skills/french-tutor)
- [Publisher profile](https://clawhub.ai/user/sharoonsharif)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Conversational Markdown with optional JSON progress data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update french-tutor-progress.json in the current working directory.]

## Skill Version(s):

4.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
