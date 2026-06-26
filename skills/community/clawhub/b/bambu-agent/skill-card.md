## Description: <br>
Monitors and manages Bambu Lab 3D printers on a local network with real-time status, error decoding, voice summaries, and a web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhouzia](https://clawhub.ai/user/Zhouzia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and agents use this skill to monitor a local Bambu Lab printer farm, answer progress and material questions, summarize active jobs, and surface printer errors without exposing full serial numbers in normal responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated config.json stores printer access codes and serial numbers. <br>
Mitigation: Keep config.json on a trusted local machine, do not commit or share it, and avoid pasting logs or screenshots that contain printer credentials. <br>
Risk: The skill continuously monitors printers on the local network when auto-start is enabled. <br>
Mitigation: Install it only on trusted networks and disable auto-start or stop the service when continuous monitoring is not wanted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Zhouzia/bambu-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and text responses grounded in local API status data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can expose local printer status summaries and web dashboard access after the user configures printer IP addresses, access codes, and serial numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
