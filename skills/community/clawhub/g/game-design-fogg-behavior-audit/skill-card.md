## Description: <br>
Audit a game feature, flow, event, onboarding step, progression action, monetization surface, retention mechanic, or social prompt using the Fogg Behavior Model: Motivation, Ability, Prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game designers, product managers, and developers use this skill to evaluate whether a game feature or flow is likely to cause a specific player behavior. It helps diagnose weak adoption, friction, timing problems, and behavioral bottlenecks across onboarding, retention, progression, social, event, and monetization surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations may affect live monetization, retention, or player-behavior systems. <br>
Mitigation: Review recommendations before applying them to production game features or player-facing flows. <br>
Risk: Prompts may include sensitive player data, credentials, or confidential telemetry. <br>
Mitigation: Use only data approved for the agent environment and avoid pasting secrets or confidential telemetry unless that environment is authorized. <br>


## Reference(s): <br>
- [Fogg Notes](references/fogg-notes.md) <br>
- [Game Examples](references/game-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown structured as target behavior, motivation read, ability read, prompt read, failure diagnosis, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask clarifying questions when the target player behavior is unclear.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
