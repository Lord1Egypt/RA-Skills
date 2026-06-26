## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding-agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockcloud](https://clawhub.ai/user/blockcloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to capture command failures, corrections, missing capabilities, outdated knowledge, and reusable best practices so future sessions can review or promote them into project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated learning files may retain sensitive session details too broadly. <br>
Mitigation: Treat learning files as sensitive and avoid storing raw prompts, secrets, tokens, customer data, full stack traces, or internal URLs. <br>
Risk: Promoting session learnings into shared agent instruction files can spread incorrect or overly specific guidance. <br>
Mitigation: Require explicit review and approval before promoting entries into shared files or sharing them across sessions. <br>
Risk: Hook-based reminders can add persistent behavioral nudges to agent sessions. <br>
Mitigation: Enable hooks only when durable agent memory is intended and review hook output before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blockcloud/cpskilltest111) <br>
- [OpenClaw integration](artifact/references/openclaw-integration.md) <br>
- [Hook setup guide](artifact/references/hooks-setup.md) <br>
- [Examples](artifact/references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminders and structured learning-entry templates; optional hooks can add short session or error-detection prompts.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
