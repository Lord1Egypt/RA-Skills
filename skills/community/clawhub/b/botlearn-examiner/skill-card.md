## Description:

Conducts standardized OpenClaw Agent capability examinations, applies rubric-based scoring across eight dimensions, and produces reports with radar charts and improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw Agent users use this skill to run structured capability exams, practice specific dimensions, score responses against rubrics, and generate capability reports for improvement planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute submitted code while scoring code-generation answers.

Mitigation: Run submitted code only in a sandbox with explicit limits, no ambient credentials, and reviewable test fixtures.

Risk: The skill stores detailed exam records that may include identifiable user history and answers.

Mitigation: Require user consent before persistence and provide clear retention, export, and deletion controls.

Risk: Broad activation phrases may trigger an exam flow unintentionally.

Mitigation: Use specific activation phrases or require confirmation before starting an examination session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/calvinxhk/skills/botlearn-examiner)
- [Publisher profile](https://clawhub.ai/user/calvinxhk)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Configuration, Guidance]

**Output Format:** [Markdown reports and prompts with JSON answer schemas, code snippets, score tables, and ASCII or SVG radar chart instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May offer JSON, Markdown, SVG, and anonymized benchmark export options.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
