## Description: <br>
Rebuilds exam papers from PDF or image inputs by combining OCR, LLM audit correction, structured question parsing, and HTML/JSON/Markdown outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, assessment teams, and education-technology developers use this skill to convert scanned or image-based exam papers into editable structured exams with review notes and multi-format outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exam files may contain confidential, copyrighted, or student-identifying information and may be processed through selected OCR or LLM services. <br>
Mitigation: Prefer local OCR for sensitive materials, avoid optional online document creation unless needed, and confirm that the selected services are approved for the data being processed. <br>
Risk: OCR and LLM correction can introduce incorrect question text, formulas, answers, or classifications. <br>
Mitigation: Review the generated audit log, manually check warning or error items, and validate the final HTML, JSON, and Markdown outputs before reuse. <br>
Risk: Generated intermediate and output files can mix source exam material with derived answers and explanations. <br>
Mitigation: Use a dedicated output folder and apply normal access controls and retention rules for exam content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/skills/exam-ocr-rebuilder) <br>
- [Question type classification standard](references/question-types.md) <br>
- [Output template](references/output-template.md) <br>
- [LLM audit prompt template](references/llm-audit-prompt.md) <br>
- [OCR tools comparison guide](references/ocr-tools-comparison.md) <br>
- [Interactive audit HTML template](references/html-template-audit.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated HTML, JSON, and Markdown exam files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured exam data, an interactive report, Markdown exam text, and audit logs when the workflow is completed.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
