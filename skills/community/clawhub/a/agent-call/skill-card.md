## Description:

Enables agents to initiate Twilio phone calls, send SMS notifications, and inspect call status using shell scripts and Twilio credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe-evolver](https://clawhub.ai/user/pe-evolver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let an agent prepare and run Twilio-based outbound call, SMS, and call-status workflows for operational communications such as appointment reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate high-impact phone and SMS actions, including recording or transcription, if credentials and inputs are available.

Mitigation: Require explicit approval before calls, SMS, recording, or transcription; test only with owned numbers; and restrict use to authorized operators.

Risk: Unsafe shell input handling can expose call, SMS, TwiML, callback, or form-encoding inputs to misuse.

Mitigation: Avoid untrusted inputs until the shell, Python, TwiML, and form-encoding issues identified by security evidence are fixed.

Risk: Twilio credentials and callback URLs can expose account privileges or route sensitive call data.

Mitigation: Use environment-injected or protected credentials and restrict callbacks to HTTPS endpoints under the user's control.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/pe-evolver/skills/agent-call)
- [Twilio Voice documentation](https://www.twilio.com/docs/voice)
- [Twilio documentation](https://www.twilio.com/docs)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can result in Twilio phone calls, SMS messages, recording, transcription, and call-status requests when the generated or referenced scripts are executed.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
