# Class Seven - Workflow Patterns

## Pattern 1: Sequential Pipeline

```
[Task] → PM → Architect → Developer → Tester → [Deliverable]
```

Use when: Clear linear progression, each phase depends on previous

### Implementation
```python
# Main Session as Manager
pm_result = spawn_agent("PM", task_description)
arch_result = spawn_agent("Architect", pm_result.output)
dev_result = spawn_agent("Developer", arch_result.output)
test_result = spawn_agent("Tester", dev_result.output)
return integrate(test_result)
```

## Pattern 2: Parallel Sprint

```
         ┌→ Developer A (Module 1)
[Task] ──┼→ Developer B (Module 2)
         └→ Developer C (Module 3)
              ↓
         Integration → Tester
```

Use when: Modules are independent, can parallelize development

### Implementation
```python
modules = break_down(task)
results = parallel_spawn([
    ("Developer", m) for m in modules
])
integrated = integrate_results(results)
return spawn_agent("Tester", integrated)
```

## Pattern 3: Iterative Refinement

```
[Requirement] → Developer → Tester → [Bugs?]
                    ↑_____________|
```

Use when: Requirements evolve, need rapid iteration

### Implementation
```python
code = spawn_agent("Developer", requirements)
for i in range(max_iterations):
    test_result = spawn_agent("Tester", code)
    if test_result.passed:
        break
    code = spawn_agent("Developer", {
        "code": code,
        "bugs": test_result.bugs
    })
```

## Pattern 4: Debug Triage

```
[Bug Report] → Debugger → [RCA]
                    ↓
            ┌───┴───┐
        [Code Fix] [Config Fix] [Env Fix]
```

Use when: Production issues, need systematic debugging

### Implementation
```python
rca = spawn_agent("Debugger", bug_report)
if rca.type == "code":
    fix = spawn_agent("Developer", rca.analysis)
elif rca.type == "config":
    fix = apply_config_fix(rca.recommendation)
elif rca.type == "environment":
    fix = spawn_agent("DevOps", rca.analysis)
```

## Pattern 5: Review Board

```
[Code/Design] → PM Review
              → Architect Review
              → Tester Review
              ↓
         Consolidated Feedback
```

Use when: Quality gates, significant changes

### Implementation
```python
reviews = parallel_spawn([
    ("PM", code),
    ("Architect", code),
    ("Tester", code)
])
feedback = consolidate_reviews(reviews)
if feedback.blocking_issues:
    return spawn_agent("Developer", {
        "code": code,
        "feedback": feedback
    })
```

## Communication Protocol

### Agent Output Format

Each agent should return:
```json
{
  "agent": "<role>",
  "status": "success|partial|failed",
  "output": "<main deliverable>",
  "artifacts": ["<file paths>"],
  "notes": "<important considerations>",
  "blockers": ["<issues requiring escalation>"]
}
```

### Context Passing Rules

1. **Minimal but sufficient** - Include only what's needed
2. **Structured format** - Use JSON/YAML for complex data
3. **Version tracking** - Include iteration number
4. **Decision log** - Record key decisions made

### Escalation Triggers

Escalate to human when:
- Agent returns status="failed" twice
- Conflicting requirements from different agents
- Scope creep beyond original task
- Technical blockers requiring architectural changes
