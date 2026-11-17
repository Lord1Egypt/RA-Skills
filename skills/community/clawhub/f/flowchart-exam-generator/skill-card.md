## Description:

Flowchart Exam Generator analyzes uploaded flowchart images and produces single-choice and multiple-choice exam questions for process-knowledge checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geming416684729-svg](https://clawhub.ai/user/geming416684729-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, trainers, and operations teams use this skill to convert readable process flowcharts into standardized exam-question spreadsheets. It is suited for creating single-choice and multiple-choice checks that include options, numeric answer keys, explanations, and source-flow references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets may be unsafe when source flowchart text comes from untrusted people or contains formula-like content.

Mitigation: Treat generated spreadsheets as untrusted, open them with external links and active content disabled, and sanitize formula-like input before sharing.

Risk: Unclear flowchart images or incomplete extraction can produce inaccurate questions, answers, or explanations.

Mitigation: Review the extracted flow steps and generated answer key against the original flowchart before using the exam.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Files, Code]

**Output Format:** [Chinese exam-question content and Excel spreadsheet files (.xlsx)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces four-option questions with numeric answer keys, explanations, and flowchart source labels.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
