## Description: <br>
ClawSoul gives an OpenClaw agent an MBTI-based personality, learns communication preferences locally, offers recommendations, and can accept Pro token based personality injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fanyur-Wang](https://clawhub.ai/user/Fanyur-Wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and skill developers use this skill to add an adaptive MBTI-style persona to an agent, persist local communication preferences, and manage personality status or injection commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local personality profiling can store user preferences, interaction patterns, and injected token data. <br>
Mitigation: Review local storage and deletion controls before enabling the skill; clear local state when the profile is no longer needed. <br>
Risk: The skill can change the assistant persona through prompt modification. <br>
Mitigation: Enable it only in contexts where behavior-changing prompts are acceptable, and inspect status plus prompt templates after personality changes. <br>
Risk: Optional LLM provider paths can send conversation excerpts to configured local or remote endpoints. <br>
Mitigation: Keep remote providers disabled or local-only when privacy matters, and confirm provider settings before use. <br>
Risk: Pro token injection accepts Base64 or JSON input and can overwrite personality state. <br>
Mitigation: Use tokens only from trusted sources and inspect token contents before injection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fanyur-Wang/clawsoul-skill-new) <br>
- [Publisher profile](https://clawhub.ai/user/Fanyur-Wang) <br>
- [Configured Pro recommendation endpoint](https://clawsoul.neural-sync.center) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text command responses with local JSON state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists MBTI, preferences, interaction patterns, adaptation level, and injected token data in local state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
