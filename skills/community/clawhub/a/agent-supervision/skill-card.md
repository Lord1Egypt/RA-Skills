## Description: <br>
Supervise another OpenClaw agent with fixed-interval check-ins or ETA-based follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z157181773](https://clawhub.ai/user/z157181773) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to supervise another OpenClaw agent through recurring or ETA-based check-ins, progress classification, and concise escalation messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A target sessionKey can expose or affect another agent session. <br>
Mitigation: Treat the sessionKey as sensitive and confirm it with the user before enabling supervision. <br>
Risk: Recurring supervision can create unwanted noise or excessive pressure if cadence and escalation are unclear. <br>
Mitigation: Verify the cron interval, progress definition, and escalation rule before scheduling recurring checks. <br>
Risk: Supervision automation may use cross-session messaging tools. <br>
Mitigation: Keep the tool allowlist limited to session history and session sending as documented. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z157181773/agent-supervision) <br>
- [Release notes](references/release-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Text] <br>
**Output Format:** [Markdown with JSON snippets and short supervision messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supervision messages use compact status codes and should stay short enough for recurring agent check-ins.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and release notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
