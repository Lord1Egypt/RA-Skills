---
name: br-risk-analyzer
category: testing
description: 根据需求文档分析风险，分析代码漏洞。analyzes code changes between commits against requirement documents to identify and prioritize risk points. 
version: 1.0
---
# BR Risk Analyzer Skill

## Overview
This skill analyzes code changes between commits against requirement documents to identify and prioritize risk points following the established code review protocol.

## Workflow Implementation

### Step 1: Input Digestion
- Extract from requirements: functional goals, non-functional requirements (performance/security), boundary conditions, prohibited behaviors, dependent systems
- Identify **key terms** as search keywords: entities, state machines, configuration items, message topics, external interfaces

### Step 2: Code Scope Definition  
- Use semantic search/grep/glob to locate: entry points (Controllers/timers/consumers), core Services, persistence layers, message handling, configuration reading
- Map **data flow** (who writes/reads: DB/Redis/MQ/files) and **control flow** (sync/async/retry patterns)

### Step 3: Requirement-Driven Code Review
For each requirement aspect, verify against code:

| Verification Dimension | Key Questions |
|------------------------|---------------|
| Correctness | Branch coverage, safe defaults, enum/state consistency |
| Boundaries | Null handling, large datasets, timeouts, duplicate submissions, idempotency |
| Concurrency | Locking, transaction boundaries, visibility, race conditions |
| Failure Paths | Exception swallowing, rollback capability, retry logic, partial failure handling |
| Configuration & Switches | Behavior when config missing, dangerous switch combinations |
| Security | Authorization, privilege escalation, injection vulnerabilities, sensitive data logging |
| Dependencies | External call failures, degradation strategies, circuit breaking, timeouts |
| Compatibility | Legacy data handling, old API support, grayscale deployment and rollback |

### Step 4: Risk Classification & Output
Follow strict priority grading:

**P0 (Must Fix)**: 
- Financial/data errors, security vulnerabilities, widespread outages, irreversible data corruption

**P1 (Fix This Iteration)**:
- Functionality errors under specific conditions, severe performance degradation, monitoring blind spots amplifying failures

**P2/P3 (Optional)**:
- Maintainability issues, edge case UX problems, low-probability exceptions, style/comment improvements

### Step 5: Knowledge Persistence
- Store analysis results and project understanding in `resources/project-understanding.md`
- Update accumulated knowledge for future risk assessments
- Maintain historical context of requirement interpretations and codebase evolution

## Usage Protocol

### Input Requirements
Provide in single message:
1. **Requirement/Design Document Summary** (or PRD highlights, change notes, interface contracts)
2. **Scope** (repository paths, modules, branches, related issue/ticket numbers)  
3. **Expected Output** (risk list only / risks + test cases / with priority and fix recommendations)

### Execution Guarantees
- **Requirement-first approach**: Use requirements to drive code examination, not random file scanning
- **Evidence-based**: Each risk includes **file path + class/method + behavior description**; mark speculation as "needs confirmation"
- **Layered risk analysis**: Interface contracts, concurrency/consistency, exception handling, configuration/data, security/compliance, performance/resources, observability, compatibility/rollback
- **Requirement alignment**: Explicitly categorize as "covered by requirements" / "not mentioned in requirements but potential issue" / "outside current scope"

## Output Template

Results follow this mandatory structure:

```markdown
## Review Summary
- Requirement highlights: (1-3 sentences)
- Code scope: (module/path list)
- Overview: P0 x items / P1 x items / P2 x items / P3 x items

## Risk Inventory

### P0 (Must Address)
| ID | Risk Description | Location (file:class/method) | Trigger Conditions/Impact | Recommendation (optional) |
|----|------------------|------------------------------|---------------------------|---------------------------|
| R1 | ... | ... | ... | ... |

### P1 (Recommend Fix This Iteration)
| ID | Risk Description | Location | Trigger Conditions/Impact | Recommendation |
|----|------------------|----------|---------------------------|----------------|
| ... | ... | ... | ... | ... |

### P2 / P3 (Discretionary)
- ...

## Requirement Coverage Assessment
- Covered: ...
- Not explicitly covered in requirements but present in code: ...
- Out of scope for this review: ...

## Testing Recommendations (Optional)
| Risk ID | Test Type | Scenario | Expected |
|---------|-----------|----------|----------|
| R1 | Integration | ... | ... |
```
The results is saved in {requirements name}-risk-analyzer.md

## Quick Checklist Integration

During review, systematically verify:
- [ ] All entry points have proper authorization/parameter validation (when required)?
- [ ] Database writes and message sending order prevent inconsistency? Need transactions or compensation?
- [ ] Async thread pools / MQ consumption failures cause data loss or duplication?
- [ ] Behavior is defined when config is empty, parsing fails, or dependent services timeout?
- [ ] Logs contain sensitive data (keys, IDs, full request bodies)?
- [ ] Large files/batches could cause OOM or thread pool exhaustion?
- [ ] State machine transitions handle illegal states properly?
- [ ] Core branches have unit/contract tests?

## Testing Guidance

- **P0/P1 risks**: Provide specific test scenarios with preconditions, key steps, expected results
- **Test classification**: Indicate suitability for unit tests / integration tests / manual regression
- **Testing complements but doesn't replace code review**: Test suggestions validate high-risk findings, not substitute logical analysis