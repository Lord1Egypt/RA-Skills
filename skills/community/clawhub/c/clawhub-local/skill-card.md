## Description: <br>
Use the ClawHub CLI to search, install, update, and publish agent skills from clawhub.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage ClawHub skills from the command line, including search, install, update, list, authentication, and publish workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global npm installation and registry selection can install unexpected CLI code or use an unintended registry. <br>
Mitigation: Review the package name and registry before installing or running commands, and override the registry only when it is trusted. <br>
Risk: Forced or all-skill updates can change installed skill behavior across a workspace. <br>
Mitigation: Avoid forced all-skill updates unless installed skills are trusted and review resolved versions before applying updates. <br>
Risk: Publish commands can upload local skill content to ClawHub. <br>
Mitigation: Confirm authentication state and review publish arguments and local skill contents before publishing. <br>


## Reference(s): <br>
- [Clawhub Local listing](https://clawhub.ai/andy27725/clawhub-local) <br>
- [ClawHub registry](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the npm-installed clawhub CLI binary for command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
