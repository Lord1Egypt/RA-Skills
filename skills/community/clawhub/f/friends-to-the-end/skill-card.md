## Description: <br>
Use when Hermes agents, profiles, or app-embedded agents need to help each other by sharing skills, tools, context, verification, and handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newsense2004](https://clawhub.ai/user/newsense2004) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate Hermes-style multi-agent handoffs, profile selection, context sharing, and result verification across profiles, apps, or services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger phrase could invite another agent or profile when the user did not clearly intend a multi-agent handoff. <br>
Mitigation: Use the skill only on explicit user intent and confirm the target profile, role, and return value before invoking another agent. <br>
Risk: Profile cloning or cross-agent prompts may expose secrets or sensitive profile context. <br>
Mitigation: Avoid cloning personal profiles with secrets unless necessary, keep API keys in profile environment files, and do not print or copy secret values into prompts or logs. <br>
Risk: Another agent may return plausible but incorrect results or claim side effects that did not happen. <br>
Mitigation: Verify returned results against files, APIs, logs, health checks, browser behavior, or other authoritative source data before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newsense2004/friends-to-the-end) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages structured return values and verification of cross-agent results before acting on them.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
