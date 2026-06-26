## Description: <br>
Index important directories and perform safe folder operations with proper security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and general users use this skill to keep a lightweight index of important local folders, discover projects in common work directories, and handle cleanup or folder operations with explicit path-safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may scan common local folders and maintain a local path index. <br>
Mitigation: Review indexed paths before approving additions and avoid indexing sensitive or unnecessary directories. <br>
Risk: Cleanup requests can change the local filesystem even when items are moved to trash. <br>
Mitigation: Review cleanup proposals before approval, especially for work folders or network drives. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/folders) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with paths, prompts, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May maintain a local JSON folder index at ~/.config/folder-index.json when the user approves updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
