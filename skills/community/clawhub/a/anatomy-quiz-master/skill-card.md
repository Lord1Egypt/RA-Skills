## Description:

Generate interactive anatomy quizzes for medical education with multiple question types, difficulty levels, and anatomical regions, supporting gross anatomy, neuroanatomy, and clinical correlations for self-assessment and exam preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External medical students, teaching assistants, and educators use this skill to generate anatomy self-assessment quizzes, practical exam practice, and clinical-correlation study materials. It is supplemental study support and is not a substitute for anatomy texts, faculty review, or cadaver lab instruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency manifest lists Python standard-library module names and can cause failed or misleading dependency installation.

Mitigation: Review or remove requirements.txt before installation; run the quiz script with the standard Python library unless valid third-party dependencies are later added.

Risk: The command-line output option can overwrite an existing writable file path.

Mitigation: Use --output only inside a dedicated workspace directory and choose a new filename for generated quiz files.

Risk: Generated anatomy questions may contain educational or clinical inaccuracies if used without subject-matter review.

Mitigation: Have anatomy faculty or qualified clinical reviewers verify question content, answer keys, and explanations before use in instruction or assessment.

## Reference(s):

- [Anatomy Quiz Master reference guidelines](references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/anatomy-quiz-master)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON or plain text quiz content, with Markdown and shell examples in the skill guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print quiz output to stdout or write it to a user-specified output file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
