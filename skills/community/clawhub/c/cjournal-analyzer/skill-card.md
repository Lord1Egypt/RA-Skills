## Description: <br>
Analyzes CSSCI (C刊) journals by collecting recent CNKI article metadata, identifying publication trends, and generating a Word report with topic, author, method, and submission guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, graduate students, and academic editors use this skill to analyze CSSCI journal publication patterns, identify topic trends and core authors, and prepare journal-level submission strategy reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CNKI browser automation may trigger verification, rate limiting, or incomplete collection. <br>
Mitigation: Supervise the browsing session, complete CNKI verification manually when prompted, and use the documented request pauses and progress checks. <br>
Risk: Generated reports may contain research metadata, abstracts, or analysis that should be reviewed before sharing. <br>
Mitigation: Choose and check the output folder, review the DOCX report and source data, and apply applicable CNKI and institutional usage requirements. <br>
Risk: The analysis script installs and runs local Python dependencies and writes report artifacts. <br>
Mitigation: Run dependencies in a virtual environment and inspect generated files before relying on or distributing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yipng05-max/cjournal-analyzer) <br>
- [CNKI journal navigation](https://navi.cnki.net/knavi/) <br>
- [CNKI journal code quick reference](references/journal_codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell snippets, JSON data, PNG charts, and DOCX report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local JSON, chart images, and a Word report from CNKI article metadata; may require supervised CNKI browser verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
