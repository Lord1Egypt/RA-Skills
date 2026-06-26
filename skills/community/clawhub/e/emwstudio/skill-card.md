## Description: <br>
Runs selected RunningHub-hosted ComfyUI workflows for multilingual sauce duck videos, "Do Not Be Afraid" videos, and "Miaojiao 2026" advertising voiceover generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emwstudio](https://clawhub.ai/user/emwstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to configure RunningHub access, choose one of the bundled ComfyUI workflow presets, provide workflow inputs, and receive task status or generated media results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a RunningHub API key in plaintext and may save or print it through local configuration and script arguments. <br>
Mitigation: Install only if the author and RunningHub are trusted, avoid exposing command output in logs or screenshots, and rotate or remove the key if it may have been exposed. <br>
Risk: Workflow inputs and API credentials are sent to RunningHub-hosted endpoints to create and query generation tasks. <br>
Mitigation: Do not submit sensitive inputs unless RunningHub is approved for the intended data, account, and workflow use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emwstudio/emwstudio) <br>
- [Publisher profile](https://clawhub.ai/user/emwstudio) <br>
- [RunningHub China service](https://www.runninghub.cn/?inviteCode=6bfdf1c0) <br>
- [RunningHub international service](https://www.runninghub.ai/?inviteCode=6bfdf1c0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown messages with JSON command results and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a RunningHub API key; may run background polling for up to 20 minutes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
