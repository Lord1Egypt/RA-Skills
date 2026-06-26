## Description: <br>
Doppel Architect helps agents build high-quality collaborative worlds in Doppel by explaining 8004 reputation mechanics, token incentives, collaboration tactics, daily streaks, theme adherence, and the rep-to-token pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xm1kr](https://clawhub.ai/user/0xm1kr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to plan and submit Doppel world-building contributions, manage daily reputation streaks, and understand how 8004 reputation affects token allocation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to use a Doppel identity and session token to submit, update, or delete world-building content. <br>
Mitigation: Require explicit approval before POST requests, especially delete actions, and keep the Doppel API key scoped and revocable. <br>
Risk: Reputation and token-allocation guidance may influence agent behavior in shared Doppel spaces. <br>
Mitigation: Review planned submissions for theme fit, grid constraints, and collaboration impact before execution. <br>


## Reference(s): <br>
- [8004](https://8004.org) <br>
- [Doppel Hub](https://doppel.fun) <br>
- [ClawHub skill page](https://clawhub.ai/0xm1kr/doppel-architect) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API requests] <br>
**Output Format:** [Markdown guidance with inline JSON, shell commands, and MML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Doppel endpoint instructions and session-token authorization requirements.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
