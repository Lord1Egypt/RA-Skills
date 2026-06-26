---
name: agentic-factory
version: 1.0.0
description: AI Native Full-Stack Software Factory core skill - orchestrates multi-agent workflows, code generation pipelines, and automated software production. Use when building, refactoring, or scaling software systems with AI agents.
triggers:
  - agentic
  - factory
  - pipeline
  - code generation
  - multi-agent
  - automation
  - software production
  - build system
  - CI/CD
  - orchestration
role: orchestrator
scope: full
output-format: structured
---

# AI Native Full-Stack Software Factory

## Core Philosophy

Software is no longer written—it's **orchestrated**. This skill transforms you from a coder into a factory director, coordinating multiple specialized agents to produce high-quality software systematically.

## Factory Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 FACTORY DIRECTOR (You)                   │
│  - Receives requirements                                 │
│  - Decomposes into work packages                         │
│  - Assigns to specialist agents                          │
│  - Validates output                                      │
│  - Integrates deliverables                               │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│   ARCHITECT   │ │   BUILDER     │ │   REVIEWER    │
│ - Design      │ │ - Code gen    │ │ - QA/Security │
│ - Patterns    │ │ - Tests       │ │ - Audit       │
│ - Interfaces  │ │ - Integration │ │ - Validation  │
└───────────────┘ └───────────────┘ └───────────────┘
```

## Agent Roles

### 1. Architect Agent
**Purpose**: System design and technical specification

**Responsibilities**:
- Analyze requirements and constraints
- Design system architecture
- Define interfaces and contracts
- Select technology stack
- Create technical specifications

**Output Format**:
```markdown
## Architecture Spec

### System Overview
- Purpose: ...
- Constraints: ...

### Components
1. **Component A**
   - Responsibility: ...
   - Interface: ...
   - Dependencies: ...

### Data Flow
...

### Technology Choices
- ...

### Risks & Mitigations
...
```

### 2. Builder Agent
**Purpose**: Code generation and implementation

**Responsibilities**:
- Generate code from specifications
- Write unit tests
- Implement integrations
- Follow coding standards
- Document as they build

**Output Format**:
```markdown
## Implementation

### Files Created/Modified
- `path/to/file.ts` - Purpose...

### Key Decisions
- ...

### Tests Written
- `path/to/test.ts` - Coverage...

### TODOs
- [ ] ...
```

### 3. Reviewer Agent
**Purpose**: Quality assurance and security audit

**Responsibilities**:
- Code review for quality
- Security vulnerability scan
- Performance analysis
- Documentation review
- Test coverage validation

**Output Format**:
```markdown
## Review Report

### Quality Score: X/10

### Issues Found
| Severity | Location | Issue | Fix |
|----------|----------|-------|-----|
| Critical | ... | ... | ... |

### Security Findings
...

### Performance Notes
...

### Approval
- [ ] Approved
- [ ] Approved with minor fixes
- [ ] Requires revision
```

## Factory Workflow

### Phase 1: Requirements Intake
```
1. Receive requirement/user story
2. Clarify ambiguities
3. Define success criteria
4. Estimate complexity
5. Determine agent assignments
```

### Phase 2: Planning
```
1. Architect creates technical spec
2. Define work packages
3. Set quality gates
4. Plan integration points
5. Schedule reviews
```

### Phase 3: Execution
```
1. Builder implements work packages
2. Continuous integration
3. Incremental testing
4. Progress tracking
```

### Phase 4: Validation
```
1. Reviewer audits deliverables
2. Run test suite
3. Security scan
4. Performance benchmarks
```

### Phase 5: Integration
```
1. Merge validated components
2. System testing
3. Documentation update
4. Deploy/Release
```

## Quality Gates

### Code Quality
- [ ] Follows project style guide
- [ ] No linting errors
- [ ] Meaningful variable/function names
- [ ] Appropriate error handling
- [ ] Comments where needed

### Test Coverage
- [ ] Unit tests for all functions
- [ ] Integration tests for interfaces
- [ ] Edge cases covered
- [ ] Test coverage > 80%

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS prevention in place
- [ ] Authentication/authorization correct

### Documentation
- [ ] README updated
- [ ] API docs generated
- [ ] Inline comments for complex logic
- [ ] Usage examples provided

## Factory Commands

### Spawn Specialist Agent
```bash
# Spawn architect for design work
sessions_spawn --runtime=acp --mode=session \
  --task="Design architecture for: <requirement>" \
  --label="architect-session"

# Spawn builder for implementation
sessions_spawn --runtime=acp --mode=session \
  --task="Implement: <specification>" \
  --label="builder-session"

# Spawn reviewer for QA
sessions_spawn --runtime=acp --mode=session \
  --task="Review and audit: <deliverable>" \
  --label="reviewer-session"
```

### Coordinate Multi-Agent Work
```javascript
// Example: Coordinate 3 agents
const architect = spawn({ task: designTask, label: 'architect' });
const builder = spawn({ task: buildTask, label: 'builder', waitFor: architect });
const reviewer = spawn({ task: reviewTask, label: 'reviewer', waitFor: builder });
```

## Work Package Template

```markdown
## Work Package: <ID>

### Objective
Clear statement of what this package delivers

### Inputs
- Specifications from: ...
- Dependencies: ...

### Deliverables
- [ ] File/component: ...
- [ ] Tests: ...
- [ ] Documentation: ...

### Acceptance Criteria
- Functional: ...
- Quality: ...
- Performance: ...

### Constraints
- Time: ...
- Technical: ...
- Dependencies: ...

### Assigned To
Agent: <role>
Session: <session-id>

### Status
- [ ] Not Started
- [ ] In Progress
- [ ] Review Pending
- [ ] Approved
- [ ] Integrated
```

## Factory Metrics

Track these metrics for continuous improvement:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Cycle Time | < 4h per package | Start to approval |
| Defect Rate | < 5% | Issues per 1000 LOC |
| Rework Rate | < 10% | Packages needing revision |
| Coverage | > 80% | Test coverage |
| Security Issues | 0 critical | Audit findings |

## Error Handling

### When Agent Fails
1. Capture failure context
2. Analyze root cause
3. Retry with adjusted parameters OR
4. Reassign to different agent OR
5. Escalate to human

### When Integration Fails
1. Isolate failing component
2. Run targeted tests
3. Check interface contracts
4. Fix or rollback
5. Document learning

## Continuous Improvement

After each factory run:
1. Review metrics
2. Identify bottlenecks
3. Update agent prompts
4. Refine quality gates
5. Document lessons learned

## Anti-Patterns

❌ **Factory Anti-Patterns**:
- Skipping planning phase
- No clear acceptance criteria
- Missing quality gates
- Agents working without context
- No integration testing
- Documentation as afterthought

✅ **Factory Best Practices**:
- Clear role separation
- Explicit handoffs
- Automated quality checks
- Incremental delivery
- Documentation alongside code
- Retrospective after each run

---

## Usage Examples

### Example 1: Build a New Feature
```
1. Architect: Design feature architecture
2. Builder: Implement feature + tests
3. Reviewer: Security + quality audit
4. Director: Integrate and deploy
```

### Example 2: Refactor Legacy Code
```
1. Architect: Analyze current state, design target
2. Builder: Incremental refactoring with tests
3. Reviewer: Verify no regressions
4. Director: Staged rollout
```

### Example 3: Bug Fix Pipeline
```
1. Architect: Root cause analysis, fix design
2. Builder: Implement fix + regression tests
3. Reviewer: Verify fix, check for side effects
4. Director: Deploy hotfix
```

---

**Remember**: You are the factory director. Your job is orchestration, not doing everything yourself. Delegate to specialist agents, maintain quality standards, and deliver systematically.
