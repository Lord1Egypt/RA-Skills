## Description: <br>
AIRILAB lets an agent use AiriLab image workflows for MJ-style generation, creative 4K upscaling, atmosphere conversion, login and project setup, asynchronous task polling, and result retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatekii](https://clawhub.ai/user/tatekii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use AIRILAB to submit AiriLab image generation, upscaling, and atmosphere conversion jobs while the skill manages login, project selection, job polling, and result delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a persistent background AiriLab worker by default. <br>
Mitigation: Review before installing; run setup with autostart disabled when continuous polling is not desired. <br>
Risk: Authentication tokens, selected project data, job state, and logs are stored locally. <br>
Mitigation: Confirm AIRILAB_HOME before use, protect that directory, and periodically remove saved tokens or job data when no longer needed. <br>
Risk: Uploaded images and generated result URLs are sent to AiriLab and written locally. <br>
Mitigation: Avoid sensitive images unless the AiriLab data handling terms fit the user's requirements. <br>


## Reference(s): <br>
- [ClawHub AIRILAB skill page](https://clawhub.ai/tatekii/airilab) <br>
- [AiriLab service](https://cn.airilab.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown or plain text status summaries with shell commands, generated result URLs, and local JSON/SQLite state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists token, project, job database, logs, and worker PID under AIRILAB_HOME or ~/.openclaw/skills/airilab.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
