## Description: <br>
Control Box2Robot robotic arms via cloud API to move servos, record trajectories with camera, download datasets, generate videos, and orchestrate AI training and inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boxjod](https://clawhub.ai/user/boxjod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and robot operators use this skill to control Box2Robot robotic arms, record and replay demonstrations, collect camera datasets, and submit or deploy robot training and inference jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move physical robotic hardware, calibrate servos, replay trajectories, and deploy inference that controls an arm. <br>
Mitigation: Use it only with owned or administered devices, keep a human operator present, verify the device and workspace before execution, and require explicit approval for motion, calibration, playback, and inference deployment. <br>
Risk: Camera and audio commands can capture privacy-sensitive data from connected peripherals. <br>
Mitigation: Ask for user consent before camera or audio capture, avoid recording private environments, and delete captured frames, audio, datasets, and cached outputs when they are no longer needed. <br>
Risk: The skill stores or uses credentials that grant device-control authority. <br>
Mitigation: Prefer interactive login, avoid placing passwords in command history, protect B2R_TOKEN and ~/.b2r_token, and delete or revoke the cached token after use. <br>
Risk: Store actions can purchase or run third-party tasks on physical hardware. <br>
Mitigation: Require explicit approval before purchases or store-run actions, review task details before execution, and run only trusted tasks on a cleared device. <br>


## Reference(s): <br>
- [ClawHub box2robot-skills release page](https://clawhub.ai/boxjod/box2robot-skills) <br>
- [Box2Robot homepage](https://robot.box2ai.com) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [SKILLS.md](SKILLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and JSON-oriented API response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, aiohttp, access to the Box2Robot cloud service, and a B2R_TOKEN or cached ~/.b2r_token for authenticated device control.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
