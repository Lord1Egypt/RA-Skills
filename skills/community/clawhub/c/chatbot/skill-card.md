## Description:

Build real-time voice chatbot applications with natural conversation flow and customizable personalities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build SenseAudio-backed voice assistants, customer service bots, educational assistants, and companion chatbots with session management and real-time voice integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SenseAudio API keys, session tokens, room IDs, and conversation IDs can expose account access or private session data if mishandled.

Mitigation: Keep credentials and session identifiers server-side where possible, avoid logging them, and rotate or revoke exposed credentials promptly.

Risk: Voice and chat sessions may be processed by SenseAudio services.

Mitigation: Inform users before collecting voice input and review data handling requirements for the intended deployment.

Risk: Generated integration code may need adaptation for production authentication, timeout, quota, and error handling requirements.

Mitigation: Review the generated code before deployment, add application-specific controls, and test network failure and quota scenarios.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scikkk/skills/chatbot)
- [SenseAudio Homepage](https://senseaudio.cn)
- [SenseAudio API Key Setup](https://senseaudio.cn/platform/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python and HTML code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration guidance for SenseAudio API sessions, real-time voice connection setup, status checks, and conversation analytics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
