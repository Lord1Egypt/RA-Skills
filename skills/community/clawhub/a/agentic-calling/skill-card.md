## Description:

Enable AI agents to make outbound calls, send SMS notifications, check call status, and manage recordings through Twilio-backed shell scripts and guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kellyclaudeai](https://clawhub.ai/user/kellyclaudeai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to add phone-call and SMS workflows to an agent, including appointment reminders, status checks, and follow-up notifications. It is suited to Twilio-based telephony tasks where credential handling, call consent, and spend controls are managed by the deploying team.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real calls and send SMS messages through Twilio, which can create cost, consent, and misuse exposure.

Mitigation: Use test or least-privilege Twilio credentials, restrict allowed destination numbers, and require human or policy approval before live outbound calling or messaging.

Risk: Untrusted message, voice, URL, media, timeout, or phone-number inputs may be handled unsafely by the packaged shell scripts.

Mitigation: Validate and constrain all user-controlled inputs before invoking scripts, and fix the scripts before using them with untrusted data.

Risk: Recording and transcription can capture sensitive call content.

Mitigation: Enable recording or transcription only after consent, retention, and access-control requirements are defined and enforced.

Risk: Twilio credentials may be exposed if stored insecurely.

Mitigation: Store credentials in a secret manager or a configuration file with 600 permissions, and avoid committing credentials to source control.

## Reference(s):

- [Agentic Calling ClawHub Skill](https://clawhub.ai/kellyclaudeai/skills/agentic-calling)
- [Artifact README](artifact/README.md)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Twilio Voice Documentation](https://www.twilio.com/docs/voice)
- [Twilio Documentation](https://www.twilio.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON configuration examples, and shell-script text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Twilio call or message identifiers, call status records, transcription text, and local recording files when the packaged scripts are run with credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
