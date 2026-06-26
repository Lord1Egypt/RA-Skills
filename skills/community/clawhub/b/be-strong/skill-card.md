## Description: <br>
Captures learnings, errors, and corrections so agents can record reusable project knowledge, command failures, missing capabilities, and workflow improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mn4223222-afk](https://clawhub.ai/user/mn4223222-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain structured learning, error, and feature-request logs that can improve future agent behavior across projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to persist broad conversation, error, and workflow learnings into future-injected memory files. <br>
Mitigation: Install only when persistent agent memory is desired, keep entries scoped to useful project knowledge, and avoid raw transcripts or private user data. <br>
Risk: Learning logs or promoted memory files may capture secrets, credentials, environment variables, or unredacted command output. <br>
Mitigation: Require redaction before logging and do not store secrets, credentials, private user data, raw transcripts, or unredacted command output. <br>
Risk: Optional hook scripts can add automatic reminders or inspect command output for error patterns. <br>
Mitigation: Keep hook use opt-in and review hook scripts before enabling them in a workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mn4223222-afk/be-strong) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Hooks setup](references/hooks-setup.md) <br>
- [Logging examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates local learning, error, and feature-request logs when the agent follows the skill workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
