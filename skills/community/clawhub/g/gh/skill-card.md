## Description: <br>
Use the GitHub CLI (gh) to perform core GitHub operations: auth status, repo create/clone/fork, issues, pull requests, releases, and basic repo management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Trumppo](https://clawhub.ai/user/Trumppo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent to run authenticated GitHub CLI workflows for repositories, issues, pull requests, releases, and basic repository management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub CLI commands can create, publish, merge, delete, or otherwise change repositories. <br>
Mitigation: Review proposed commands and confirm the target owner and repository before execution, especially for organization or production repositories. <br>
Risk: Authenticated gh operations use the current user's GitHub permissions. <br>
Mitigation: Run gh auth status before sensitive workflows and use the least-privileged account or token suitable for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Trumppo/gh) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with inline shell commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report GitHub URLs or command results after gh operations complete.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
