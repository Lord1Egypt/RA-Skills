## Description:

English Learning Coach turns an agent into an immersive English conversation coach that checks learner messages before replying, gives correction-only feedback when needed, controls output vocabulary level, tracks vocabulary and recurring errors, estimates CEFR level, runs mini quizzes, and summarizes progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taxueqinyin](https://clawhub.ai/user/taxueqinyin)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and employees use this skill for English conversation practice with lightweight correction routing, simple-level agent replies, recurring-error review, active vocabulary tracking, CEFR estimates, and short progress checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save local records of practice text, mistakes, scores, vocabulary, CEFR estimates, and quiz history without showing routine persistence notices.

Mitigation: Install only when local learning records are acceptable; avoid sensitive personal or workplace content unless storage location, retention, and deletion controls are clarified.

Risk: Stored learner text may be reused in later reviews or summaries without sanitization.

Mitigation: Review stored Markdown and practice data before reuse, and prefer a version that sanitizes stored content before using it in future review commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taxueqinyin/skills/english-learning-coach-txqy)
- [Publisher profile](https://clawhub.ai/user/taxueqinyin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown responses, with optional shell commands and JSON-backed local learning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Correction-only responses use a fixed Correction/Reason/Natural version shape; review commands can summarize scores, CEFR estimates, vocabulary, quizzes, and stored practice history.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
