## Description: <br>
Lists available audio input devices and helps diagnose whether microphones and other input devices are working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to list available microphone devices, confirm valid input device IDs, and troubleshoot common PyAudio audio input failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to propose or run local diagnostic commands for audio device enumeration. <br>
Mitigation: Review proposed commands before execution and do not grant credentials or write access unless it is required for the intended diagnostic task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/audio-device-diagnostic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example diagnostic output and troubleshooting guidance for selecting an audio input device.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
