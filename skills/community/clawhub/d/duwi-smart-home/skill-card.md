## Description: <br>
Duwi Smart Home helps agents use the Duwi Open Platform API to query homes, rooms, devices, scenes, and sensor data, and to control Duwi-connected smart-home devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duwi2024](https://clawhub.ai/user/duwi2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a Duwi smart-home account, including choosing a home, listing rooms and devices, querying device status, running scenes, and issuing device-control commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control physical Duwi-connected devices such as lights, curtains, climate systems, breakers, and scenes. <br>
Mitigation: Review the intended action before execution, prefer exact device numbers or precise room and device names, and confirm that the target device is online and correct. <br>
Risk: Application keys, secrets, account passwords, access tokens, and local JSON credential files may expose access to the smart-home account. <br>
Mitigation: Use interactive secret entry where possible, avoid passing passwords or APPKEY/SECRET values in shell commands, and protect or remove local credential and token files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/duwi2024/duwi-smart-home) <br>
- [Duwi Open Platform API endpoint](https://openapi.duwi.com.cn/homeApi/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cause authenticated API calls that control physical smart-home devices when the generated commands are executed.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
