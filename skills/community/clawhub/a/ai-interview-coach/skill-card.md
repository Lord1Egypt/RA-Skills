## Description:

AI-powered interview preparation assistant with three difficulty levels, flexible question counts, five question types, interview history tracking, progress analysis, capability radar charts, 7-day sprint plans, job readiness scoring, answer rewriting, document generation mode, and interactive mock interview mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hogozhang](https://clawhub.ai/user/hogozhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare for job interviews by generating targeted interview questions, practicing mock interviews, assessing readiness, improving answers, and tracking interview practice progress from resumes or role descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read resumes that users explicitly provide.

Mitigation: Redact unnecessary personal details from resumes before use and provide only the resume content needed for interview preparation.

Risk: The skill may keep local practice history in ~/.ai-interview-coach/history.json.

Mitigation: Review or delete the local history file when practice records should not be retained.

Risk: The documented npx installation command is not pinned.

Mitigation: Use a pinned or manual install path when release reproducibility is required.

## Reference(s):

- [AI-Interview-Coach on ClawHub](https://clawhub.ai/hogozhang/skills/ai-interview-coach)
- [Publisher profile: hogozhang](https://clawhub.ai/user/hogozhang)
- [README](artifact/README.md)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance, Analysis]

**Output Format:** [Markdown with interview questions, reference answers, scoring summaries, practice plans, answer rewrites, and optional code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-provided resumes and may store local interview practice history for progress tracking.]

## Skill Version(s):

5.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
