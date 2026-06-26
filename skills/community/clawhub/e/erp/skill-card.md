## Description: <br>
Plan resources, track inventory, and coordinate departments with reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to keep local ERP-style notes for resource planning, inventory tracking, department coordination, reminders, reports, and weekly reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ERP notes are stored as plaintext files in ~/.local/share/erp. <br>
Mitigation: Avoid entering passwords, secrets, regulated personal data, or highly confidential business records unless appropriate filesystem protections and retention controls are in place. <br>
Risk: Export files may contain sensitive operational notes. <br>
Mitigation: Review JSON, CSV, or TXT exports before sharing them outside the intended audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/erp) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plaintext log, export, status, and search output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local plaintext files under ~/.local/share/erp and can export JSON, CSV, or TXT files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
