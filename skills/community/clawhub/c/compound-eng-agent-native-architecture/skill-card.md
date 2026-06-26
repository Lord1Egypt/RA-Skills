## Description: <br>
Design agent-native applications where agents replace UI users as the primary actor, including MCP tools, agent-loop architectures, shared-workspace file patterns, and self-modifying agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design or review agent-native systems, with guidance for architecture, tools, shared workspaces, prompts, context injection, self-modification, mobile execution, hooks, and testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture examples may encourage broad agent powers such as unrestricted reads, generic API calls, publishing, git push or deploy workflows, and self-modifying prompts. <br>
Mitigation: Require explicit user consent, workspace scoping, review gates, audit logs, and rollback controls before implementing those patterns. <br>
Risk: Examples involving user content, analytics logs, HealthKit, iCloud workspaces, or other personal data can expose secrets or PII if copied directly into a product. <br>
Mitigation: Apply secret and PII redaction, least-privilege access, and clear data boundaries before using the guidance in an implementation. <br>


## Reference(s): <br>
- [Action Parity Discipline](references/action-parity-discipline.md) <br>
- [Agent Execution Patterns](references/agent-execution-patterns.md) <br>
- [Agent-Native Testing](references/agent-native-testing.md) <br>
- [Anti-Patterns](references/anti-patterns.md) <br>
- [Architecture Patterns](references/architecture-patterns.md) <br>
- [Core Principles](references/core-principles.md) <br>
- [Dynamic Context Injection](references/dynamic-context-injection.md) <br>
- [Files Universal Interface](references/files-universal-interface.md) <br>
- [From Primitives to Domain Tools](references/from-primitives-to-domain-tools.md) <br>
- [Hooks Patterns](references/hooks-patterns.md) <br>
- [MCP Tool Design](references/mcp-tool-design.md) <br>
- [Mobile Cost](references/mobile-cost.md) <br>
- [Mobile Execution](references/mobile-execution.md) <br>
- [Mobile Patterns](references/mobile-patterns.md) <br>
- [Mobile Storage](references/mobile-storage.md) <br>
- [Product Implications](references/product-implications.md) <br>
- [Quick Start](references/quick-start.md) <br>
- [Refactoring to Prompt Native](references/refactoring-to-prompt-native.md) <br>
- [Self Modification](references/self-modification.md) <br>
- [Shared Workspace Architecture](references/shared-workspace-architecture.md) <br>
- [Success Criteria](references/success-criteria.md) <br>
- [System Prompt Design](references/system-prompt-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with checklists, examples, code snippets, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill routes the agent to focused reference material based on the user's selected architecture topic.] <br>

## Skill Version(s): <br>
4.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
