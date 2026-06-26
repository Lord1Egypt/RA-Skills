## Description: <br>
Game Dev Assistant helps game developers analyze game data, manage level and asset workflows, automate Unity builds, parse saves, and review logs across Unity, Unreal, and Godot projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaochunz030-spec](https://clawhub.ai/user/xiaochunz030-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and game teams use this skill to inspect game configuration data and logs, organize project assets, and prepare build or test automation for game projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unity build automation and custom build methods can run local engine commands against project files. <br>
Mitigation: Verify the Unity executable, project path, output path, target platform, and build method before execution, and run builds in a controlled workspace. <br>
Risk: Game logs, data files, saves, and asset reports may contain proprietary or sensitive project information. <br>
Mitigation: Review inputs and generated reports before sharing them, and keep backups before any save, asset, or project-file modification workflow. <br>
Risk: Generated build, test, or configuration guidance may not match a specific project's engine version or platform requirements. <br>
Mitigation: Inspect generated commands and files before use, then validate them on a non-production branch or test project first. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, JSON reports, and generated helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local project paths, game data files, build outputs, and log reports supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
