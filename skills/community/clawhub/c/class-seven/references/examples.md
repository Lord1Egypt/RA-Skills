# Class Seven - Example Projects

## Example 1: REST API Development

### Task
Build a user management REST API with authentication

### Team Deployment
```
Manager: You (Main Session)
├─ PM: Define API requirements, endpoints, auth strategy
├─ Architect: Design data models, middleware structure
├─ Developer: Implement FastAPI app with JWT auth
├─ Tester: Write pytest tests, test coverage
└─ [No Debugger needed - clean build]
```

### Tool Selection
| Agent | Tool | Reason |
|-------|------|--------|
| PM | Kimi | Bilingual requirements doc |
| Architect | Claude Code | Design pattern decisions |
| Developer | Kimi | Fast implementation |
| Tester | Native | Deterministic test execution |

### Execution
```python
# Main Session
pm_spec = sessions_spawn(
    task="Design REST API for user management with JWT auth",
    model="kimi-coding/k2p5",
    label="pm-api"
)

arch_design = sessions_spawn(
    task=f"Design FastAPI architecture for: {pm_spec.output}",
    model="anthropic/claude-sonnet-4-5",
    label="arch-api"
)

code = sessions_spawn(
    task=f"Implement FastAPI app based on: {arch_design.output}",
    model="kimi-coding/k2p5",
    label="dev-api"
)

test_result = sessions_spawn(
    task=f"Write tests for: {code.output}",
    label="test-api"
)
```

## Example 2: Bug Investigation

### Task
Investigate intermittent 500 errors in production

### Team Deployment
```
Manager: You (Main Session)
├─ Debugger: Analyze logs, identify root cause
├─ Developer: Implement fix
└─ Tester: Verify fix, regression tests
```

### Tool Selection
| Agent | Tool | Reason |
|-------|------|--------|
| Debugger | Claude Code | Deep log analysis |
| Developer | Kimi | Quick patch |
| Tester | Native | Automated testing |

### Execution
```python
# Main Session
rca = sessions_spawn(
    task="""Analyze these production logs for 500 errors:
    <logs attached>
    Identify root cause and provide fix strategy""",
    model="anthropic/claude-sonnet-4-5",
    label="debugger-500"
)

fix = sessions_spawn(
    task=f"Implement fix for: {rca.root_cause}",
    model="kimi-coding/k2p5",
    label="dev-fix"
)

verify = sessions_spawn(
    task=f"Verify fix and write regression tests: {fix.output}",
    label="test-verify"
)
```

## Example 3: Code Review Workflow

### Task
Review PR #42 for security and best practices

### Team Deployment
```
Manager: You (Main Session)
├─ PM: Check against requirements
├─ Architect: Review design patterns
└─ Tester: Check test coverage, edge cases
```

### Tool Selection
| Agent | Tool | Reason |
|-------|------|--------|
| PM | Kimi | Requirement alignment |
| Architect | Claude Code | Pattern analysis |
| Tester | Kimi | Edge case identification |

### Execution
```python
# Fetch PR content first
pr_content = fetch_pr(42)

reviews = [
    sessions_spawn(
        task=f"Review PR against requirements: {pr_content}",
        model="kimi-coding/k2p5",
        label="review-pm"
    ),
    sessions_spawn(
        task=f"Review design patterns: {pr_content}",
        model="anthropic/claude-sonnet-4-5",
        label="review-arch"
    ),
    sessions_spawn(
        task=f"Review tests and edge cases: {pr_content}",
        model="kimi-coding/k2p5",
        label="review-test"
    )
]

consolidated = consolidate_reviews(reviews)
```

## Example 4: Legacy Code Migration

### Task
Migrate Python 2 codebase to Python 3

### Team Deployment
```
Manager: You (Main Session)
├─ PM: Define migration scope, risk assessment
├─ Architect: Design migration strategy
├─ Developer: Execute migration (multiple spawns for modules)
├─ Tester: Comprehensive test suite
└─ Debugger: Handle edge cases, compatibility issues
```

### Tool Selection
| Agent | Tool | Reason |
|-------|------|--------|
| PM | Kimi | Scope definition |
| Architect | Claude Code | Strategy design |
| Developer | Claude Code | Complex refactoring |
| Tester | Native | Batch testing |
| Debugger | Claude Code | Compatibility fixes |

### Execution
```python
# Phase 1: Planning
scope = sessions_spawn("Define migration scope", model="kimi-coding/k2p5")
strategy = sessions_spawn(f"Design strategy for: {scope}", model="anthropic/claude-sonnet-4-5")

# Phase 2: Parallel migration
modules = identify_modules("./legacy-code")
migration_results = []
for module in modules:
    result = sessions_spawn(
        task=f"Migrate {module} using strategy: {strategy}",
        model="anthropic/claude-sonnet-4-5",
        label=f"dev-migrate-{module}"
    )
    migration_results.append(result)

# Phase 3: Testing & Debugging
all_code = merge_results(migration_results)
tests = sessions_spawn(f"Test migrated code: {all_code}")

if tests.failed:
    fixes = sessions_spawn(f"Fix failures: {tests.failures}")
```

## Example 5: New Feature - Full Pipeline

### Task
Add "advanced search" feature to existing app

### Complete Workflow
```python
# Main Session orchestration

def class_seven_full_pipeline(task_description):
    """Execute full Class Seven workflow"""
    
    # Phase 1: PM
    prd = sessions_spawn(
        task=f"""As PM, create PRD for: {task_description}
        Include: user stories, acceptance criteria, scope""",
        model="kimi-coding/k2p5",
        label="pm-prd"
    )
    
    # Phase 2: Architect
    design = sessions_spawn(
        task=f"""As Architect, design system for:
        {prd.output}
        Include: tech stack, data models, API specs""",
        model="anthropic/claude-sonnet-4-5",
        label="arch-design"
    )
    
    # Phase 3: Developer
    code = sessions_spawn(
        task=f"""As Developer, implement:
        {design.output}
        Follow coding standards, add comments""",
        model="kimi-coding/k2p5",
        label="dev-impl"
    )
    
    # Phase 4: Tester
    qa = sessions_spawn(
        task=f"""As Tester, verify:
        Code: {code.output}
        Against: {prd.acceptance_criteria}
        Include: test cases, bug report if any""",
        model="kimi-coding/k2p5",
        label="test-qa"
    )
    
    # Phase 5: Debug (conditional)
    if qa.bugs:
        fixed = sessions_spawn(
            task=f"Fix these bugs: {qa.bugs}",
            model="anthropic/claude-sonnet-4-5",
            label="debug-fix"
        )
        code = fixed.output
    
    # Integration
    deliverable = {
        "prd": prd.output,
        "design": design.output,
        "code": code.output,
        "tests": qa.test_cases,
        "status": "complete" if not qa.bugs else "fixed"
    }
    
    return deliverable

# Execute
result = class_seven_full_pipeline("Add advanced search with filters and sorting")
```

## Success Metrics

Track these for workflow optimization:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Delivery rate | >90% | Completed / Attempted |
| Bug escape rate | <5% | Production bugs / Total bugs |
| Time to delivery | Varies by complexity | From task to deliverable |
| Cost per task | Optimized | Total tokens / Task |
| Human intervention | <10% | Escalations / Total tasks |
