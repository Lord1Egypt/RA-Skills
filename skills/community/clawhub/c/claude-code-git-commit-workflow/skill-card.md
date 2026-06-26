## Description: <br>
Helps an agent create one clean git commit from current changes with safe staging, concise message drafting, and non-interactive git usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they want an agent to inspect a working tree, stage only relevant changes, draft a concise message, and create one non-amended commit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrelated work or secrets could be staged if the working tree is not reviewed before committing. <br>
Mitigation: Inspect the working tree and staged files before commit creation, and keep unrelated or sensitive files unstaged. <br>
Risk: The final commit message could misrepresent the change if accepted without review. <br>
Mitigation: Review the drafted commit message against the staged diff before allowing the commit to be created. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and a commit summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one non-amended git commit when applicable; avoids empty commits, amend flows, hook bypasses, secrets, and unrelated files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
