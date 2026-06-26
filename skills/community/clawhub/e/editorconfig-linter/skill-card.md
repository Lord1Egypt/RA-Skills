## Description: <br>
Validate .editorconfig syntax and check source files for EditorConfig compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate .editorconfig files, check source files for EditorConfig compliance, inspect effective rules, and optionally apply narrow formatting fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-fix mode can unintentionally change formatting across many project files when run broadly. <br>
Mitigation: Use check mode first, run fix only on a narrow path in a version-controlled workspace, and review the diff before committing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/editorconfig-linter) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Shell commands, Guidance, Files] <br>
**Output Format:** [Plain text, JSON, or Markdown lint reports; fix mode writes formatting changes to matched files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports strict CI exit codes, exclude patterns, max-file limits, and auto-discovery of .editorconfig files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter: 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
