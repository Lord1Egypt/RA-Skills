## Description: <br>
This instruction-only skill helps OpenClaw-style agents improve repeated work through structured reflection while preserving user approval, privacy, scope, memory, tool, and policy boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a disciplined self-review loop to agent work. It guides agents to observe outcomes, identify small improvements, and ask for approval before changes affect future behavior, memory, files, tools, policies, or permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may try to persist memory, change files, alter tools or policies, add automation, or apply improvements beyond the current task. <br>
Mitigation: Require explicit user approval before any improvement affects future behavior, memory, files, tools, policies, permissions, automation, or task scope. <br>
Risk: Review payloads could expose private or sensitive information if copied verbatim. <br>
Mitigation: Use minimal redacted summaries and exclude secrets, tokens, passwords, full payment data, unnecessary private records, and unrelated user messages. <br>
Risk: Marketplace capability tags indicate crypto and purchase capabilities even though the security evidence describes an instruction-only self-review skill. <br>
Mitigation: Ignore those unrelated tags unless the publisher corrects them, and review any future behavior that would enable purchases, crypto handling, external calls, or tool changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-continuous-improvement) <br>
- [Review payload schema](schemas/improvement-cycle.schema.json) <br>
- [Redacted improvement-cycle example](examples/redacted-improvement-cycle.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown instructions with a short optional text report and optional JSON review payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no bundled code, dependency installation, command execution, file writes, memory persistence, or external service calls by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
