## Description: <br>
Maps application security findings to OWASP Top 10 categories and generates remediation checklists for normalized AppSec review outputs and category-level prioritization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security engineers, and AppSec reviewers use this skill to normalize raw security findings into OWASP Top 10 categories, aggregate them by severity, and produce remediation checklist output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local mapper writes report output to the path provided by the user, which can overwrite or create files in that location. <br>
Mitigation: Use a new, non-critical output path and review the destination before running the script. <br>
Risk: The current --dry-run option is recorded in output details but does not prevent the report file from being written. <br>
Mitigation: Do not rely on --dry-run to avoid writes; run only with an output path where file creation is acceptable. <br>


## Reference(s): <br>
- [OWASP Mapping Guide](references/owasp-mapping-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/0x-Professor/cyber-owasp-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or CSV report content with normalized finding rows, category counts, and remediation checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled mapper reads a local findings JSON file and writes a report to a user-selected output path.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
