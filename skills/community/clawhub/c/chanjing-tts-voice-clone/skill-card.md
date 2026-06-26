## Description: <br>
Uses the Chanjing TTS API to clone a user-provided reference voice from a public audio URL, synthesize speech from text, poll asynchronous jobs, and return generated audio download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamzn1018](https://clawhub.ai/user/iamzn1018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create a custom Chanjing voice from authorized reference audio and generate Chinese or English speech from text. It is suited to workflows that need scripted voice-clone TTS with task polling and returned audio URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates local Chanjing credentials, including access_token and expire_in. <br>
Mitigation: Keep ~/.chanjing/credentials.json private, do not commit it to version control, and use CHANJING_CONFIG_DIR only for trusted credential storage. <br>
Risk: Reference audio and synthesis text are sent to Chanjing for processing. <br>
Mitigation: Use only voice material and text that the user is authorized to send to the Chanjing service. <br>
Risk: Changing CHANJING_API_BASE redirects credentialed requests to another endpoint. <br>
Mitigation: Set CHANJING_API_BASE only when the replacement API endpoint is deliberately trusted. <br>


## Reference(s): <br>
- [Chanjing API Documentation](https://doc.chanjing.cc) <br>
- [ClawHub Skill Page](https://clawhub.ai/iamzn1018/chanjing-tts-voice-clone) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and command-line output, including voice IDs, task IDs, and generated audio URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Chanjing credentials and network access to the configured Chanjing API endpoint.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
