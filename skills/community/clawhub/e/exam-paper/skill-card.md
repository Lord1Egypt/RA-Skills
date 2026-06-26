## Description: <br>
Exam Paper helps an agent build exam papers from local question banks, manage questions, track wrong answers, and generate exam and answer-key PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kreator666](https://clawhub.ai/user/kreator666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, students, and exam-preparation users can use this skill through an agent to assemble practice exams, maintain subject question banks, and review wrong-answer records. It is especially oriented toward informatics olympiad-style question formats while allowing other subjects to be added. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted subject names or imported question-bank JSON may cause reads or writes outside the advertised exam-data folder. <br>
Mitigation: Use only trusted question files, avoid subject names containing slashes or '..', and review commands before creating, importing, exporting, or modifying local data. <br>
Risk: The skill creates or modifies local question-bank, wrong-answer, JSON, and PDF files. <br>
Mitigation: Run it in a controlled workspace and confirm output directories before allowing file-writing commands. <br>


## Reference(s): <br>
- [Exam Format Reference](references/exam-formats.md) <br>
- [Informatics Topic Reference](references/informatics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with Python CLI commands; generated outputs can include JSON exam data and PDF exam files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python execution and reportlab for PDF generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
