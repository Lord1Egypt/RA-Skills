## Description: <br>
Compare contract templates with scanned stamped contracts, list all differences (additions, deletions, modifications), and output a Word report for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russell-yu](https://clawhub.ai/user/russell-yu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, legal operations teams, and developers use this skill to compare a contract template against a scanned signed contract and identify additions, deletions, and modified text. It is intended to produce review artifacts, not replace human legal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently install Python packages during execution. <br>
Mitigation: Run it in an isolated virtual environment or disposable workspace and review dependencies before use. <br>
Risk: Helper scripts may overwrite fixed local filenames such as template.docx and scanned.pdf. <br>
Mitigation: Keep backups of input contracts and run the skill in a separate working directory. <br>
Risk: Contracts and generated reports may contain confidential information. <br>
Mitigation: Use only approved storage and handling locations, and avoid highly confidential contracts unless outputs are secured. <br>
Risk: OCR-based comparison can miss or misclassify contract changes. <br>
Mitigation: Treat reports as review aids and manually verify critical clauses before acting on the results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/russell-yu/contract-diff) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Sample markdown report](artifact/output/report.md) <br>
- [Detailed sample report](artifact/output/详细比对报告.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Word document report with optional Markdown report and highlighted image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compares Word or PDF templates with scanned PDF or image contracts using OCR; reported differences require human review because OCR and matching can be inaccurate.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
