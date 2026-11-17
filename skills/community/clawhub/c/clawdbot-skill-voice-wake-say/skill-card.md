## Description:

Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake or voice recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xadenryan](https://clawhub.ai/user/xadenryan)

### License/Terms of Use:


## Use Case:

Developers and agent users on macOS use this skill to have voice-initiated assistant responses spoken locally after an exact Voice Wake prefix is detected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spoken output can reveal response contents to people nearby.

Mitigation: Install and use the skill only when local audible responses are intended, and rely on the exact-prefix trigger so ordinary text requests remain silent.

Risk: The local macOS `say` command may be unavailable or may fail.

Mitigation: Return the text response and notify the user that text-to-speech failed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xadenryan/skills/clawdbot-skill-voice-wake-say)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with local shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local macOS speech output only when the exact Voice Wake prefix is present; otherwise the agent responds with text only.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
