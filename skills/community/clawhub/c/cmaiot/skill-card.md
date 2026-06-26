## Description: <br>
Queries and controls products and devices on the China Mobile AIoT platform (iot.10086.cn), including video live-stream URL retrieval for supported devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ch2925](https://clawhub.ai/user/ch2925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to let an agent inspect China Mobile AIoT product models, query device state, manage device enablement, set properties, call services, and retrieve video device playback URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real China Mobile AIoT devices, including setting properties, invoking services, creating devices, and enabling or disabling devices. <br>
Mitigation: Confirm exact product IDs, device names, requested actions, and JSON payloads before running set, call, create, enable, or disable commands. <br>
Risk: The skill stores product API keys locally in a generated config.json file. <br>
Mitigation: Protect the generated config.json file, limit access to trusted users, and rotate keys if the file or command output may have been exposed. <br>
Risk: The skill can reveal video device live-stream URLs and raw API responses. <br>
Mitigation: Avoid sharing live-stream URLs or full command output outside trusted contexts. <br>
Risk: Real-time property reads, property writes, and service calls require online devices and can fail or time out. <br>
Mitigation: Check device status first, skip offline or nonexistent devices, and treat device-control timeouts as failed operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ch2925/cmaiot) <br>
- [Publisher profile](https://clawhub.ai/user/ch2925) <br>
- [China Mobile AIoT platform](https://iot.10086.cn) <br>
- [China Mobile AIoT API endpoint](https://iot-api.heclouds.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured device-operation summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live device status, API responses, device-control results, and video stream URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
