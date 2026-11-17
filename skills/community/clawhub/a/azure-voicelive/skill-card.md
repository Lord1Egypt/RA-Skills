## Description: <br>
Azure VoiceLive Pro helps agents guide developers through enterprise real-time voice AI setup, including function calling, custom voices, telephony audio formats, session handling, and interruption handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to configure Azure VoiceLive-based voice agents for customer service, telephony, function-tool integration, custom voice use, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad read, write, and command-execution authority. <br>
Mitigation: Approve commands and file changes explicitly, and run the skill only in environments where those capabilities are acceptable. <br>
Risk: Voice, caller, transcript, and phone-number data may require privacy controls that are not fully specified by the artifact. <br>
Mitigation: Add caller consent, phone-number masking, transcript and log retention controls, and access restrictions before real calls. <br>
Risk: Azure credentials and service endpoints are required for the workflow. <br>
Mitigation: Use environment variables or managed identity, avoid committing secrets, and restrict credential scope to the intended Azure resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-voicelive) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Azure VoiceLive configuration guidance, SDK usage examples, troubleshooting steps, and security reminders.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
