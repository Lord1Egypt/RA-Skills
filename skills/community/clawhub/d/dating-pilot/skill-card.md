## Description: <br>
Tinder dating assistant - swipe with filters (age/distance), conversation manager with smart replies, follow-up messaging. Use when user wants help managing their Tinder profile and conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seraphetx](https://clawhub.ai/user/seraphetx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to manage Tinder activity from a logged-in browser session, including filtered swiping, chat monitoring, smart replies, proactive follow-ups, and profile photo diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A closed-source npm package can operate a logged-in Tinder session, including swiping and sending messages. <br>
Mitigation: Use a dedicated browser profile, keep --like-count and --max-chats small, review behavior frequently, and stop the chat manager when finished. <br>
Risk: Conversation data is sent to the user-configured AI endpoint for smart replies and photo diagnosis. <br>
Mitigation: Use a trusted AI endpoint and a dedicated scoped API key instead of a primary or broadly privileged key. <br>


## Reference(s): <br>
- [Dating Pilot on ClawHub](https://clawhub.ai/seraphetx/dating-pilot) <br>
- [tinder-automation npm package](https://www.npmjs.com/package/tinder-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate through a logged-in browser session and may run as a long-running background task.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
