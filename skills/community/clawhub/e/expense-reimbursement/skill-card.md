## Description: <br>
Organizes travel reimbursement materials by scanning receipts and ZIP archives, classifying taxi, train, flight, and hotel records, filling reimbursement forms, and generating local print-ready PDF packages with user confirmation checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorwaleroy](https://clawhub.ai/user/lorwaleroy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operations staff use this skill to prepare travel reimbursement packages from local receipts, application screenshots, and reimbursement templates. It helps an agent organize trip folders, extract receipt details, request required confirmations, and produce PDFs for printing and signature workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow processes sensitive travel, receipt, project code, and reimbursement form data. <br>
Mitigation: Run it only on a dedicated reimbursement folder containing intended files, and review generated PDFs before submission. <br>
Risk: ZIP archive processing can expose unintended files if mixed with unrelated or untrusted archives. <br>
Mitigation: Avoid untrusted ZIP archives and keep only reimbursement source files in the working folder. <br>
Risk: Generated memory summaries can retain private reimbursement details. <br>
Mitigation: Delete or relocate the ~/memory summary when it contains private information. <br>
Risk: Local Python dependencies are required for document and PDF handling. <br>
Mitigation: Install dependencies in a virtual environment before running reimbursement scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lorwaleroy/expense-reimbursement) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Workflow Reference](artifact/references/workflow.md) <br>
- [Receipt Parsing Script](artifact/scripts/unzip_and_parse.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python snippets; local output files include organized folders, completed forms, and PDF print packages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local receipt files and user confirmation before key workflow stages; generated reimbursement summaries may contain sensitive personal or travel details.] <br>

## Skill Version(s): <br>
3.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
