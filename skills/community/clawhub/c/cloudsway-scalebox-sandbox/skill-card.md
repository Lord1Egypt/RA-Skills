## Description: <br>
Create and manage isolated ScaleBox cloud sandboxes for secure remote code execution, browser automation, and temporary development workflows through CLI, REST API, or Python SDK guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloriathepenguin](https://clawhub.ai/user/gloriathepenguin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, operate, and clean up isolated ScaleBox sandboxes for running commands, moving files, testing code, and browser automation away from the local machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ScaleBox API key grants account-level authority for sandbox actions. <br>
Mitigation: Store SCALEBOX_API_KEY securely, avoid exposing it in logs or shared files, and install the skill only when the ScaleBox account and publisher are trusted. <br>
Risk: Uploaded files and executed commands run in a third-party cloud sandbox environment. <br>
Mitigation: Upload only files intended for ScaleBox, review commands before execution, and avoid sending sensitive data unless the environment is approved for that use. <br>
Risk: Sandbox internet access and remote execution can increase exposure when running untrusted workloads. <br>
Mitigation: Disable sandbox internet access when unnecessary and use short-lived sandboxes with explicit cleanup after results are collected. <br>
Risk: Terminating or deleting a sandbox can remove needed outputs. <br>
Mitigation: Download required results before terminating or deleting the sandbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gloriathepenguin/cloudsway-scalebox-sandbox) <br>
- [ScaleBox official website](https://www.scalebox.dev) <br>
- [ScaleBox documentation](https://www.scalebox.dev/docs) <br>
- [ScaleBox CLI installation](https://www.scalebox.dev/docs/en/cli/installation) <br>
- [ScaleBox API reference](https://www.scalebox.dev/docs/en/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance centers on ScaleBox sandbox lifecycle, file transfer, command execution, port access, and cleanup workflows.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence.json release.version and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
