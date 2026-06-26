## Description: <br>
Helps developers write and validate strict Conventional Commits v1.0.0 while keeping commits atomic and aligned with Trunk-Based Development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omaression](https://clawhub.ai/user/omaression) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill when preparing commits, reviewing branch scope, splitting mixed changes, and validating commit messages before commit or pull request review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Git hook can block local commits in repositories that do not use these exact commit-message rules. <br>
Mitigation: Install the hook only in repositories where strict local validation is desired; otherwise run the Python validator manually when needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/omaression/commit-message-writing) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline command examples and Conventional Commit message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional local validation script and commit-msg hook instructions.] <br>

## Skill Version(s): <br>
1.0.0-alpha (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
