## Description: <br>
根据当前任务需求，使用 ClawHub 搜索、筛选并安装最合适的技能；支持指定版本安装与安装后验证。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoxiaofeng44](https://clawhub.ai/user/zhaoxiaofeng44) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to search ClawHub for task-relevant skills, compare concise recommendations, install a selected skill or version, and verify the installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing a recommended skill can add new behaviors or permissions to the agent environment. <br>
Mitigation: Check the exact slug, version, publisher, and added behavior before approving installation. <br>
Risk: Broad update commands can change multiple installed skills at once. <br>
Mitigation: Use targeted install or update commands unless intentionally updating all installed skills. <br>


## Reference(s): <br>
- [ClawHub Installer skill page](https://clawhub.ai/zhaoxiaofeng44/clawhub-installer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise recommendations and installation or verification commands for ClawHub skills.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
