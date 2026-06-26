## Description: <br>
Guides agents to suggest the /fix-npm-vuln workflow when users ask about npm audit results, vulnerable dependencies, or fixing npm package security issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jelllove](https://clawhub.ai/user/jelllove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill when a Node.js project needs npm vulnerability remediation guidance, audit triage, dependency updates, and post-fix build or test verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill allows silent installation of global npm tools or OS-level packages when they are considered low risk. <br>
Mitigation: Require the agent to show every global npm, winget, or OS package-manager install command and get user approval before running it. <br>
Risk: Automated vulnerability remediation can change dependencies, lockfiles, branches, and project behavior. <br>
Mitigation: Review dependency, lockfile, and branch changes before merging, then run the documented build and test verification steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jelllove/fix-npm-vuln) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
