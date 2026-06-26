## Description: <br>
滴答清单任务管理。管理你的滴答清单任务，包括查看项目、创建任务、完成任务、查询完成历史等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuperOwenX](https://clawhub.ai/user/SuperOwenX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure and run the dida365 command-line tool for Dida365/TickTick task management, including listing projects, creating and completing tasks, reviewing completed work, and syncing task data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses credentials and a copied session cookie for access to a task account. <br>
Mitigation: Install only when task-account access is expected, keep the session cookie out of shared terminals, scripts, logs, screenshots, and shell history, and remove stored credentials when finished. <br>
Risk: Commands can modify task-account data, including creating and completing tasks. <br>
Mitigation: Use a test or low-risk account where practical and review intended task changes before running modifying commands. <br>


## Reference(s): <br>
- [Dida365 Web App](https://dida365.com) <br>
- [Dida365 Developer Platform](https://developer.dida365.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/SuperOwenX/dida365-ticktick-agent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides CLI setup and usage commands for managing Dida365/TickTick task data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
