## Description: <br>
Manage manually installed skills (non-ClawHub). Supports checking updates, updating, and listing custom skills from GitHub or local sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qvshuo](https://clawhub.ai/user/qvshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check, list, and update manually installed skills from GitHub or local sources while keeping ClawHub-installed skills out of scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change manually installed skill files when updates are approved. <br>
Mitigation: Review the proposed change summary or diff before approving any update. <br>
Risk: Untrusted registry entries could point the updater at unsafe or unwanted sources. <br>
Mitigation: Keep REGISTRY.yaml limited to trusted GitHub or local sources. <br>
Risk: GitHub operations require authenticated CLI access. <br>
Mitigation: Use a minimally scoped GitHub login where possible and stop if authentication fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qvshuo/custom-skills-updater) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize pending updates or proposed file changes for user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
