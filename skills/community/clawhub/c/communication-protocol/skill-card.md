## Description: <br>
Defines how the OpenClaw agent should communicate with Tidy during a build session, ensuring clear, predictable, and build-focused interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DweikAnas](https://clawhub.ai/user/DweikAnas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to standardize OpenClaw communication with Tidy during build sessions, including structured progress events, concise user-facing messages, clarification questions, and terminal status events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan found no suspicious behavior in available inputs, but deeper review was limited by the available artifact evidence. <br>
Mitigation: Inspect the skill files and requested permissions before use, especially for commands, network access, credential handling, or persistent storage. <br>
Risk: Incorrect implementation of the event contract could cause confusing progress updates or expose transport metadata in user-facing messages. <br>
Mitigation: Validate emitted events against the documented payload shapes and review chat output to confirm transport headers are not repeated to users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DweikAnas/communication-protocol) <br>
- [Publisher profile](https://clawhub.ai/user/DweikAnas) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown with JSON event examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines event names, payload shapes, message-frequency rules, and language guardrails for agent communication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
