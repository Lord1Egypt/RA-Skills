## Description: <br>
Controls DuoPlus Android cloud phones through ADB broadcast commands for tapping, swiping, typing, screenshots, and UI inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duoplusofficial](https://clawhub.ai/user/duoplusofficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to connect OpenClaw to a DuoPlus or Android cloud phone, inspect the current UI, and issue controlled device actions through ADB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a connected DuoPlus or Android device and may act inside real logged-in apps. <br>
Mitigation: Use explicit device IDs, keep sensitive sessions supervised, and confirm each action with a screenshot or UI dump before continuing. <br>
Risk: Screenshots and UI hierarchy dumps may contain sensitive app or account information. <br>
Mitigation: Store local screenshots and UI dump files only as long as needed for analysis, then delete them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/duoplusofficial/duoplus-agent) <br>
- [DuoPlus Official Website](https://www.duoplus.net/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires adb and optionally cwebp; action commands are fire-and-forget and should be verified with screenshots or UI dumps.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
