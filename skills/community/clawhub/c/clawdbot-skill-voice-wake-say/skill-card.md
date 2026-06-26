## Description: <br>
Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xadenryan](https://clawhub.ai/user/xadenryan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to have an agent acknowledge and speak responses aloud for a narrowly defined Voice Wake trigger on macOS while keeping non-triggered conversations text-only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken responses may disclose sensitive conversation details to nearby listeners. <br>
Mitigation: Avoid triggering the skill for sensitive conversations when others may hear the audio. <br>
Risk: The local `say` command may be unavailable or fail on non-macOS systems. <br>
Mitigation: Fall back to the normal text response and notify the user that text-to-speech failed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xadenryan/clawdbot-skill-voice-wake-say) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local macOS text-to-speech with `say` only when the latest message begins with the configured voice-recognition trigger.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
