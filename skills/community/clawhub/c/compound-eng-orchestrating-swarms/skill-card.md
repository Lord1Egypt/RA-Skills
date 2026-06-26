## Description: <br>
Coordinates multi-agent swarms for parallel reviews, pipeline workflows, and divide-and-conquer implementation patterns with subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multiple Claude Code agents for larger code reviews, implementation pipelines, and parallel analysis while preserving file ownership and integration discipline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Writable background agents can create conflicting edits when multiple implementation tasks touch the same files. <br>
Mitigation: Use the documented one-owner-per-file rule, pre-dispatch file-intersection checks, and worktree isolation for parallel implementation work. <br>
Risk: Persistent teammates and local coordination state may remain after an orchestrated workflow completes. <br>
Mitigation: Follow the documented shutdown, orphaned-teammate checks, and cleanup steps after integration. <br>
Risk: Subagent outputs can be incomplete, blocked, or misaligned with the requested task. <br>
Mitigation: Use the documented status signals, BLOCKED triage decision tree, two-stage review gate, and retry limits before integrating outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Release Page](https://clawhub.ai/iliaal/compound-eng-orchestrating-swarms) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Specification](artifact/SPEC.md) <br>
- [Agent Types](artifact/references/agent-types.md) <br>
- [Anti-Sycophancy](artifact/references/anti-sycophancy.md) <br>
- [Context Carry-Forward](artifact/references/context-carry-forward.md) <br>
- [Dispatch Anti-Patterns](artifact/references/dispatch-anti-patterns.md) <br>
- [Environment Config](artifact/references/environment-config.md) <br>
- [Handoff Templates](artifact/references/handoff-templates.md) <br>
- [Message Formats](artifact/references/message-formats.md) <br>
- [Orchestration Patterns](artifact/references/orchestration-patterns.md) <br>
- [Primitives](artifact/references/primitives.md) <br>
- [Quick Reference](artifact/references/quick-reference.md) <br>
- [Resilience Patterns](artifact/references/resilience-patterns.md) <br>
- [Spawn Backends](artifact/references/spawn-backends.md) <br>
- [Task System](artifact/references/task-system.md) <br>
- [Team Compositions](artifact/references/team-compositions.md) <br>
- [Teammate Operations](artifact/references/teammate-operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with structured task prompts, tables, and inline command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce agent prompts, handoff templates, file-ownership plans, dispatch decisions, and cleanup steps.] <br>

## Skill Version(s): <br>
4.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
