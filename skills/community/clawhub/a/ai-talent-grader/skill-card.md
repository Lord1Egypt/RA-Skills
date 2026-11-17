## Description:

Evaluates AI-role candidates from resumes, job descriptions, and interview records with resume audit findings, L1-L4 capability grading, contradiction analysis, and follow-up interview questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Hiring teams and interviewers use this skill to review AI candidate materials, identify resume claims that need verification, grade AI-era capability levels, and generate interview follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive applicant materials and can save generated reports by default.

Mitigation: Use only with explicit permission to process applicant materials, keep candidate files and reports in a controlled directory, and delete reports according to the hiring-data retention policy.

Risk: Dependency installation may introduce supply-chain exposure.

Mitigation: Install in a virtual environment and pin or review dependencies before use.

Risk: Untrusted candidate IDs or output paths could cause reports to be written to unintended locations.

Mitigation: Avoid untrusted candidate IDs and output paths, and constrain generated reports to an approved working directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/ai-talent-grader)
- [L1-L4 behavioral anchors](references/behavioral_anchors.md)
- [Scoring calibration cases](references/calibration-cases.md)
- [Cognitive review engine](references/cognitive_review.md)
- [Evaluation matrices](references/evaluation_matrices.md)
- [Interview modules](references/interview_modules.md)
- [Output templates](references/output_templates.md)
- [Resume audit guide](references/resume_audit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports, optional JSON summaries, candidate grading tables, and interview follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports resume-only audits, full resume-plus-interview grading, cognitive interview review, batch summaries, and configurable evaluation weights.]

## Skill Version(s):

3.3.2 (source: ClawHub release evidence; bundled artifact metadata reports 3.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
