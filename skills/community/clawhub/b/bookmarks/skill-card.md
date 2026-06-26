## Description: <br>
Build a unified bookmark system that imports saves from all your platforms into one organized, actionable collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to gather saved items from connected platforms into a local searchable bookmark workspace, then tag, search, and optionally summarize those saves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can aggregate private saved items from multiple connected accounts into a persistent local archive. <br>
Mitigation: Connect only intended platforms, keep imports limited to explicit saves, and avoid likes or sensitive accounts unless the user intentionally enables them. <br>
Risk: Background importing and local storage can retain personal browsing interests longer than expected. <br>
Mitigation: Confirm the user can pause syncing, disconnect sources, and delete ~/bookmarks/ before relying on the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/bookmarks) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local ~/bookmarks/ workspace with saves, sources, preferences, and optional reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
