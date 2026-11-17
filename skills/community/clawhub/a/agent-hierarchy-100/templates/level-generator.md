# Level Generator

> Generate any level agent from 1 to 100 instantly.

---

## Usage

```
"Generate Level 042 agent for [domain]"
"Create Level 077 agent for [task]"
"Build Level 100 agent for [purpose]"
```

## Generation Protocol

```
INPUT: Level N (1-100), Domain D

STEP 1: Determine Tier
→ T1: N = 1-16
→ T2: N = 17-33
→ T3: N = 34-50
→ T4: N = 51-66
→ T5: N = 67-83
→ T6: N = 84-100

STEP 2: Load Tier Template
→ Load tier definition
→ Load capability matrix
→ Load quality gates

STEP 3: Customize for Domain
→ Apply domain-specific frameworks
→ Apply domain-specific tools
→ Apply domain-specific standards

STEP 4: Set Level-Specific Parameters
→ Reasoning depth = f(N)
→ Framework count = f(N)
→ Tool mastery = f(N)
→ Autonomy = f(N)
→ Creativity = f(N)

STEP 5: Generate Agent Files
→ config.md
→ capabilities.md
→ protocols.md
→ quality.md
→ README.md

STEP 6: Validate
→ Run quality gates
→ Verify completeness
→ Test with sample task
```

## Capability Functions

```python
# Reasoning Depth (1-10)
def reasoning_depth(level):
    return min(10, max(1, level // 10 + 1))

# Framework Count
def framework_count(level):
    return min(50, max(1, level // 2))

# Tool Mastery (0-10)
def tool_mastery(level):
    return min(10, max(0, (level - 10) // 9))

# Autonomy (1-10)
def autonomy(level):
    return min(10, max(1, level // 10 + 1))

# Creativity (0-10)
def creativity(level):
    return min(10, max(0, (level - 20) // 8))

# Max Subagent Level
def max_subagent(level):
    return max(1, level - 1)

# Context Budget (%)
def context_budget(level):
    if level <= 10:
        return 10
    elif level <= 50:
        return 30
    else:
        return 60
```

## Level Config Template

```yaml
---
level: {N}
tier: {TIER}
identity: {IDENTITY}
domain: {DOMAIN}

# Capabilities
reasoning_depth: {DEPTH}/10
framework_count: {COUNT}
tool_mastery: {MASTERY}/10
autonomy: {AUTONOMY}/10
creativity: {CREATIVITY}/10

# Hierarchy
parent_level: {PARENT}
max_subagent_level: {MAX_SUB}
can_create_agents: {CAN_CREATE}

# Resources
context_budget: {BUDGET}%
max_concurrent_subagents: {MAX_CONCURRENT}
tool_access: {TOOLS}

# Quality
quality_threshold: {THRESHOLD}/100
escalation_trigger: {TRIGGER}

# Metadata
created: {DATE}
version: 1.0.0
status: active
---
```
