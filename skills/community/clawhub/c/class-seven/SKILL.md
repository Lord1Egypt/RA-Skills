---
name: class_seven
description: Multi-agent development team workflow skill. Use when coordinating complex development tasks requiring multiple specialized roles - PM, Architect, Developer, Tester, Debugger. Orchestrates sub-agents as a development team with main session as manager. Supports flexible tool selection (Claude Code, Kimi, native tools) based on task characteristics.
---

# Class Seven - Multi-Agent Development Team

Class Seven (七班) is a structured multi-agent workflow that treats sub-agents as specialized development team members.

## When to Use

Use this skill when:
- Complex development tasks requiring multiple perspectives/roles
- Tasks needing PM planning + architecture + implementation + testing
- Debugging scenarios requiring systematic investigation
- Code review and quality assurance workflows
- Projects requiring end-to-end delivery (plan → build → test → deploy)

## Team Structure

```
Main Session (Manager)
├── PM Agent (产品经理)
├── Architect Agent (架构师)
├── Developer Agent (开发工程师)
├── Tester Agent (测试工程师)
└── Debugger Agent (调试专家)
```

## Workflow Phases

### Phase 1: Task Analysis & Planning
1. **Manager (Main Session)** analyzes task complexity
2. Spawn **PM Agent** for requirement clarification
3. PM returns: requirements doc, scope, acceptance criteria

### Phase 2: Architecture & Design
1. Spawn **Architect Agent** with PM output
2. Architect returns: tech stack, module design, interfaces

### Phase 3: Implementation
1. Spawn **Developer Agent** with architecture specs
2. Developer returns: implemented code

### Phase 4: Quality Assurance
1. Spawn **Tester Agent** with code + requirements
2. Tester returns: test plan, test cases, bugs found

### Phase 5: Debugging (if needed)
1. Spawn **Debugger Agent** with bug reports
2. Debugger returns: root cause analysis, fixes

### Phase 6: Integration & Delivery
1. Manager reviews all outputs
2. Integrates final deliverable
3. Validates against acceptance criteria

## Tool Selection Matrix

| Task Type | Primary Tool | Secondary Tool | Reason |
|-----------|-------------|----------------|--------|
| Complex architecture | Claude Code | Kimi | Deep reasoning, context management |
| Quick prototyping | Kimi | Native | Fast iteration, lower latency |
| Deep debugging | Claude Code | Kimi | Multi-file analysis, bug tracing |
| Code review | Kimi | Claude Code | Pattern recognition, best practices |
| Testing | Native | Kimi | Deterministic execution |
| Documentation | Kimi | Native | Chinese/English bilingual |

## Agent Personas

### PM Agent
```
Role: 产品经理
Expertise: Requirements analysis, user stories, acceptance criteria
Output: PRD, user stories, scope definition
Tools: Kimi (for Chinese context), Claude Code (for complex products)
```

### Architect Agent
```
Role: 架构师
Expertise: System design, tech stack selection, API design
Output: Architecture doc, module diagrams, interface specs
Tools: Claude Code (preferred for architecture), Kimi (for validation)
```

### Developer Agent
```
Role: 开发工程师
Expertise: Code implementation, refactoring, optimization
Output: Production-ready code
Tools: Claude Code (complex logic), Kimi (quick implementation), Native (boilerplate)
```

### Tester Agent
```
Role: 测试工程师
Expertise: Test design, edge case identification, quality assurance
Output: Test cases, test scripts, bug reports
Tools: Native (execution), Kimi (test design), Claude Code (complex scenarios)
```

### Debugger Agent
```
Role: 调试专家
Expertise: Root cause analysis, performance profiling, bug fixing
Output: RCA report, patches, prevention recommendations
Tools: Claude Code (deep analysis), Kimi (pattern matching)
```

## Execution Modes

### Mode A: Full Team (Full Orchestration)
All 5 phases executed sequentially. Use for complex projects.

### Mode B: Sprint Team (Dev + Test)
Skip PM/Architect phases. Use when requirements are clear.

### Mode C: Firefighter (Debug Only)
Debugger agent only. Use for urgent bug fixes.

### Mode D: Review Board (PM + Tester)
Code review workflow. Use for quality gates.

## Quick Commands

```bash
# Full team deployment
class_seven deploy --mode=full --task="<description>"

# Sprint mode
class_seven deploy --mode=sprint --specs="<requirements>"

# Debug mode
class_seven deploy --mode=debug --bug="<bug description>"
```

## Best Practices

1. **Always start with task analysis** - Determine mode and required agents
2. **Pass context explicitly** - Each agent receives relevant previous outputs
3. **Set clear boundaries** - Define what each agent should/shouldn't do
4. **Use appropriate timeout** - Complex tasks need longer timeouts
5. **Review before integration** - Manager validates all outputs

## Error Handling

If an agent fails or produces insufficient output:
1. Analyze failure reason
2. Respawn with clearer instructions or different tool
3. Consider breaking task into smaller sub-tasks
4. Escalate to human if stuck after 2 retries

## References

- Detailed workflow patterns: See [references/workflows.md](references/workflows.md)
- Tool integration guide: See [references/tools-guide.md](references/tools-guide.md)
- Example projects: See [references/examples.md](references/examples.md)
