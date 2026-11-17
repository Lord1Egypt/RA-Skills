## Description:

Provides Chinese-language exam error analysis for single questions, whole-paper loss analysis, variant question generation, and error-type guided review across K12 and vocational education.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education staff use this skill to analyze student exam papers or individual incorrect answers, generate targeted variant exercises, and prepare structured classroom feedback. It also supports vocational education scenarios that require attention to job standards, operation steps, and safety-critical mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local HTML reports may contain user-derived student or exam content, and the security summary notes unclear safeguards against active HTML injection.

Mitigation: Use only content the user is comfortable saving locally, choose the save location deliberately, and review generated HTML for escaping and blocked active scripts before opening or sharing reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyboat403/skills/exam-paper-error-analysis)
- [Server-resolved GitHub Provenance](https://github.com/flyboat403/exam-paper-error-analysis/tree/main/skills/exam-paper-error-analysis)
- [HTML Report Structure](artifact/references/html-template.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [HTML document with inline CSS]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a complete report with fixed analysis sections, navigation anchors, and print-friendly styling; saves to a user-specified directory or the current working directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
