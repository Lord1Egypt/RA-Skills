## Description: <br>
Context Memory Optimizer helps OpenClaw agents reduce context overflow, memory drift, and token waste in long-running sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donnieclaw](https://clawhub.ai/user/donnieclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to organize OpenClaw workspace memory, manage token-driven compaction, restore key context after compaction, and coordinate multi-agent handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious and notes possible guidance related to avoiding static-analysis detection. <br>
Mitigation: Review references/prompt-cache.md before installing and require any scanner-avoidance wording to be removed or reframed as normal false-positive handling. <br>
Risk: The skill can guide agents to write persistent memory files, including overwriting the current task snapshot. <br>
Mitigation: Review the declared workspace paths before use, keep memory files out of synced repositories when they may contain private context, and back up context.md if history is needed. <br>


## Reference(s): <br>
- [Context Memory Optimizer on ClawHub](https://clawhub.ai/donnieclaw/context-memory-optimizer) <br>
- [Compression Examples](references/compression-examples.md) <br>
- [Prompt Cache Optimization](references/prompt-cache.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with code blocks and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents and operators to create or update OpenClaw memory files and optional agent configuration snippets; no shell commands are issued by the skill itself.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
