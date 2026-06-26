## Description: <br>
Maintains conversation state and project continuity across sessions by saving, restoring, and managing project contexts and progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deus-pandora](https://clawhub.ai/user/deus-pandora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users working across multiple projects use this skill to restore prior session context, track pending tasks, switch active projects, and summarize where work left off. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project context, notes, pending tasks, recent files, and recent commands are stored locally and restored across sessions. <br>
Mitigation: Use only for work where that local persistence is acceptable, and periodically review or clean the stored JSON files. <br>
Risk: The artifact documents a fixed local storage path for project memory. <br>
Mitigation: Review and adjust the storage path for the target environment before deployment. <br>


## Reference(s): <br>
- [Context Engine API Reference](references/API.md) <br>
- [Context Engine ClawHub Page](https://clawhub.ai/deus-pandora/deus-pandora-context-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown responses plus JSON project and session records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local project and session state under the documented projects directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
