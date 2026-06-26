## Description: <br>
Install and configure ClawJobs for OpenClaw peer collaboration, connecting peers to a user-supplied hub for task sharing, status sync, and diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ustczz](https://clawhub.ai/user/ustczz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install the ClawJobs plugin, configure it with their own hub URL and token, inspect current settings, and diagnose connection issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ClawJobs hub token is stored in local OpenClaw configuration and may be exposed if configuration or diagnostic output is shared. <br>
Mitigation: Treat the hub token as a credential, avoid sharing logs or config output that may include it, and rotate the token if it is exposed. <br>
Risk: Connecting to an untrusted hub can expose collaboration activity or direct the plugin to an unintended remote service. <br>
Mitigation: Use only hub values you trust, provide the hub URL and token explicitly, and use the public demo only when deliberately evaluating it. <br>


## Reference(s): <br>
- [ClawJobs on ClawHub](https://clawhub.ai/ustczz/clawjobs) <br>
- [ClawJobs GitHub README public test hub](https://github.com/gtoadio-cyber/openclaw-clawjobs#public-test-hub) <br>
- [ClawJobs npm package](https://www.npmjs.com/package/clawjobs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install the ClawJobs plugin and update local OpenClaw configuration after the user provides hub values.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
