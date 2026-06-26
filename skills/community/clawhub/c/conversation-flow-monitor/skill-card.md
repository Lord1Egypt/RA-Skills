## Description: <br>
Monitors and prevents conversation flow issues by implementing robust error handling, timeouts, and recovery mechanisms for reliable agent interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edkuo7](https://clawhub.ai/user/edkuo7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor long-running agent interactions, add timeout-aware wrappers, log conversation health, and recover from common stuck states such as browser hangs, missing files, network timeouts, and cascading workflow failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete shared local log files during heartbeat cleanup. <br>
Mitigation: Restrict cleanup to this skill's own log files and disable automatic heartbeat cleanup unless needed. <br>
Risk: The skill encourages persistent workspace changes such as updates to .learnings, SOUL.md, TOOLS.md, or similar files. <br>
Mitigation: Require explicit user approval before writing or promoting persistent workspace changes. <br>
Risk: Wrapped tool calls may log context that contains sensitive information. <br>
Mitigation: Avoid wrapping calls that carry secrets and review log contents before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/edkuo7/conversation-flow-monitor) <br>
- [README](artifact/README.md) <br>
- [Usage examples](artifact/examples.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local monitoring logs and structured error dictionaries when its wrappers are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
