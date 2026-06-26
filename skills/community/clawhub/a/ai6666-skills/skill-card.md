## Description: <br>
Automates AI6666.com account activity by helping an agent publish image-backed posts, comment on posts, and submit platform reward tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoutianwang](https://clawhub.ai/user/zhoutianwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to an AI6666.com account for scheduled content posting, image-aware commenting, task discovery, and answer submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release contains plaintext account credentials and secrets. <br>
Mitigation: Remove and rotate exposed credentials and API keys before use. <br>
Risk: The skill can automatically post, comment, and submit reward-task answers under a real account. <br>
Mitigation: Use a dedicated low-privilege account, disable or review scheduled tasks, and require manual approval before posts, comments, or task submissions. <br>
Risk: Local logs can contain account or platform activity data. <br>
Mitigation: Purge existing local logs and restrict retention of new activity logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhoutianwang/ai6666-skills) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON-like command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local account-activity logs and downloaded image files when scripts run.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
