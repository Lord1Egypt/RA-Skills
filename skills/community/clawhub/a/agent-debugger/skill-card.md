## Description: <br>
Debug AI agent issues systematically, including tool failures, infinite loops, context overflow, rate limits, memory issues, permission errors, and performance bottlenecks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engsathiago](https://clawhub.ai/user/engsathiago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to diagnose misbehaving agents and choose practical fixes for loops, failed tools, context limits, rate limits, memory setup, permissions, and slow execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The debugging guidance includes advice that could expose internal reasoning or verbose agent traces. <br>
Mitigation: Do not enable hidden or internal reasoning visibility; use user-safe diagnostics and externally reviewable logs instead. <br>
Risk: Verbose logging of prompts, tool arguments, tool results, or memory contents could disclose credentials or private data. <br>
Mitigation: Redact sensitive values, avoid logging raw prompts and private file contents, and keep memory writes and tool-permission changes narrow, temporary, and explicitly user-approved. <br>


## Reference(s): <br>
- [Agent Debugger on ClawHub](https://clawhub.ai/engsathiago/agent-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not call tools or require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
