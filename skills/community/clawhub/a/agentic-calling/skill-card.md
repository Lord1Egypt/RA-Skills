## Description: <br>
Enable AI agents to autonomously make, receive, transcribe, route, and record phone calls using Twilio with customizable voice messages and IVR support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and developers use this skill to initiate Twilio calls and SMS messages for appointment reminders, emergency alerts, lead qualification, call-status checks, and recording or transcription workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Twilio credentials to place real phone calls and send SMS messages, which can contact external recipients and create account charges. <br>
Mitigation: Require human approval for call and SMS execution, maintain recipient allowlists, and configure usage and spend limits before enabling agent use. <br>
Risk: Recording and transcription features can capture sensitive conversation content. <br>
Mitigation: Apply consent rules for recording and transcription, retain logs for auditability, and restrict access to downloaded recordings and transcripts. <br>
Risk: Twilio credentials may be stored in a local config file or environment variables. <br>
Mitigation: Use restrictive permissions for credential files, avoid committing credentials, and rotate credentials if exposure is suspected. <br>
Risk: Untrusted message text may be unsafe until the documented TwiML/Python encoding issue is fixed. <br>
Mitigation: Avoid passing untrusted message text into call generation, or sanitize and review messages before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kellyclaudeai/agentic-calling) <br>
- [Twilio Voice documentation](https://www.twilio.com/docs/voice) <br>
- [Twilio documentation](https://www.twilio.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text or JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate real Twilio calls, SMS messages, recordings, downloads, and account charges when executed.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
