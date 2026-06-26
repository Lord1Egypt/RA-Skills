## Description: <br>
Use this skill when the user wants to operate Airtap or complete a request through a mobile app on an Airtap device. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skills-airtap](https://clawhub.ai/user/skills-airtap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to delegate mobile-app tasks to Airtap devices, monitor task progress, provide follow-up input, cancel tasks, and update location when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, cancel, and continue mobile-app automation tasks that may change account or app state. <br>
Mitigation: Prefer explicit $airtap invocation and confirm task creation, cancellation, continuation, and location updates before running commands. <br>
Risk: A long-lived Airtap personal access token may be stored locally in scripts/.env. <br>
Mitigation: Avoid pasting tokens into chat or shell history, restrict permissions on scripts/.env or use an external secret store, and rotate the token if exposed. <br>
Risk: Unpinned Python dependencies can change behavior between installs. <br>
Mitigation: Pin reviewed versions of requests and python-dotenv before production use. <br>
Risk: OpenClaw progress mirroring can disclose task progress to an unintended destination if routing values are wrong. <br>
Mitigation: Use OpenClaw delivery only when explicitly requested and use only routing values supplied or approved by the user. <br>


## Reference(s): <br>
- [OpenClaw Relay](references/openclaw.md) <br>
- [Airtap app](https://airtap.ai/app) <br>
- [Airtap Cortex API](https://airtap.ai/cortex/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON task responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include local polling summaries and optional OpenClaw progress updates.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
