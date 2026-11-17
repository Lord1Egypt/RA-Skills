## Description:

Travel Expense Reimbursement helps agents organize taxi, train, flight, hotel, and related reimbursement materials by scanning receipt folders and ZIP files, extracting receipt details, classifying trips, filling reimbursement forms, and generating print-ready PDF packages with user confirmation checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorwaleroy](https://clawhub.ai/user/lorwaleroy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and administrative users use this skill to assemble travel reimbursement packets from local receipt folders, validate trip classifications and totals, and prepare PDF materials for printing and signature. It is aimed at workflows that require human confirmation before filing, cleanup, print package creation, and signed-form finalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive travel and financial documents while recursively scanning reimbursement folders and ZIP archives.

Mitigation: Use a narrowly scoped reimbursement directory, review files before processing archives, and run the skill only on reimbursement materials intended for this workflow.

Risk: ZIP extraction can expose users to unsafe or untrusted archive contents.

Mitigation: Avoid untrusted archives and inspect ZIP contents before allowing the agent to scan or extract them.

Risk: The workflow stores a reimbursement summary under ~/memory that may contain employer, travel, project, or payment details.

Mitigation: Delete or disable the memory summary when those details should not persist after the reimbursement task is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorwaleroy/skills/expense-reimbursement)
- [Workflow reference](artifact/references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, file paths, and generated PDF/file organization instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow guidance and file-generation steps; PDF packages, reimbursement forms, summaries, and organized folders are created by the agent when the user confirms each stage.]

## Skill Version(s):

3.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
