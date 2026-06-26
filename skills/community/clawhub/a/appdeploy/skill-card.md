## Description: <br>
Deploy web apps with backend APIs, database, file storage, AI operations, authentication, realtime, and cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avimak](https://clawhub.ai/user/avimak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use AppDeploy to publish or update web apps with a public URL, retrieve deployment templates, check build status and logs, and manage deployed app versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads app files to an external deployment service and can expose unintended project contents if files are not reviewed first. <br>
Mitigation: Review the files being uploaded and keep secrets out of app files before deployment. <br>
Risk: The skill stores an AppDeploy API key locally in .appdeploy. <br>
Mitigation: Keep .appdeploy private, add it to .gitignore, and avoid sharing or committing the API key. <br>
Risk: The skill can overwrite or delete an existing hosted app. <br>
Mitigation: Require explicit confirmation before deleting or overwriting an app, and verify app status after changes. <br>


## Reference(s): <br>
- [AppDeploy on ClawHub](https://clawhub.ai/avimak/appdeploy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl commands, JSON payloads, file changes, deployment status, and logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload app files to AppDeploy, persist local API credentials in .appdeploy, and return hosted app status or source snapshots.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
