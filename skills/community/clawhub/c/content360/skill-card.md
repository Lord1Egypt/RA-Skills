## Description: <br>
Integrates with Content360 to create, schedule, and publish social media content across Facebook, LinkedIn, X, Instagram, YouTube, TikTok, Pinterest, Reddit, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noesis-boss](https://clawhub.ai/user/noesis-boss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content and operations teams use this skill to connect a Notion content calendar with Content360, prepare social posts, schedule publishing, and manage supported social accounts from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on a Content360 workspace and a Notion content calendar using sensitive credentials. <br>
Mitigation: Store credentials only in the intended secret manager, replace publisher-specific values with the user's own workspace values, and verify the target Content360 organization and Notion database before running. <br>
Risk: A real sync can create external social content records and mark Notion pages as posted. <br>
Mitigation: Start with the documented dry-run mode, review the selected platforms and target accounts, then run without dry-run only when those changes are intended. <br>


## Reference(s): <br>
- [Content360 ClawHub page](https://clawhub.ai/noesis-boss/content360) <br>
- [Content360 app](https://app.content360.io) <br>
- [Content360 access tokens](https://app.content360.io/os/profile/access-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Content360 and Notion credentials supplied through environment variables or the host secret manager.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
