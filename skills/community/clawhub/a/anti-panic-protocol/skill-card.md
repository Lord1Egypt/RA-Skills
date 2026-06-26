## Description: <br>
Handle tool failures under pressure with bounded retries, clean user communication, and safe escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoelisTired](https://clawhub.ai/user/NoelisTired) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to handle failed commands or tools with bounded retries, clear user updates, and safe escalation when further attempts could create duplicate actions, spam, or security risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to summarize failures instead of exposing raw stack traces or internal payloads, which can hide diagnostic detail during troubleshooting. <br>
Mitigation: Ask explicitly for full diagnostic detail or inspect logs in an appropriate private channel when deeper debugging is required. <br>
Risk: Repeated retries after command or tool failure can cause duplicate external actions, spam, or rate-limit pressure. <br>
Mitigation: Follow the two-attempt limit, respect cooldowns, and escalate clearly before making further attempts. <br>
Risk: Failures involving destructive actions, duplicate sends, authentication, or security boundaries can become unsafe if retried automatically. <br>
Mitigation: Escalate immediately in those cases and wait for an explicit next action from the user. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown and plain-language response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no tools, API keys, or external services are declared.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
