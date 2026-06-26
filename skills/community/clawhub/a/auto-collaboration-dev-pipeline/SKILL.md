---
name: auto-collaboration-dev-pipeline
description: Fully automated collaborative code development pipeline for complex code development tasks. Must be used when users request code development, program writing, feature implementation, or have code quality requirements.
---

# Fully Automated Collaborative Code Development Pipeline

A fully automated collaborative development pipeline. The main agent acts as the Project Manager (PM), orchestrating 7 sub-agent roles, advancing by phase. Users do not need to confirm midway; the final result is delivered directly.

## Applicable Scenarios

- Complex feature development (50+ lines of code, multiple files, testing required)
- Projects requiring UI/frontend design (HTML/CSS/JS, React/Vue, etc.)
- Tasks with code quality requirements (review, testing, documentation needed)
- Critical/strategic code (requires multi-person oversight)
- Users who don't want mid-process confirmation and only want to see the final result.

## Role Definitions

| # | Role | Responsibility | Phase |
|---|------|---------------|-------|
| 1 | Requirements Analyst | Parse user requirements → Output structured technical specifications | S1 |
| 2 | Architect | Design system architecture, tech stack, file structure, component tree | S2 |
| 3 | Backend Developer | Implement core business logic, data processing, APIs | S3 |
| 4 | Frontend/UI Developer | Implement interfaces, CSS styles, interaction logic | S3 |
| 5 | QA Engineer | Write and execute test cases, output test report | S4 |
| 6 | Code Reviewer | Review code quality, standards, security, performance | S5 |
| 7 | Documentation Engineer | Write README, comments, usage instructions | S6 |
| 8 | Integration/Delivery Engineer (PM) | Final integration, issue fixes, packaging and delivery | S7 |

## Pipeline Phases

```
S1 Requirements Analysis ──→ S2 Architecture Design ──→ S3 Parallel Development ──→ S4 Testing
                                            │ (backend+frontend)           │
                                            └──────────────────────────────┘
                                                          ↓
S5 Code Review ──→ S6 Documentation ──→ S7 Integration & Delivery → 📦 Final Artifact
```

## Execution Rules

### General Rules

1. **No-Interruption Principle**: Fully automated advancement; do not ask the user for confirmation. Report a progress summary after each phase is completed.
2. **Context Passing**: Each phase's sub-agent receives the complete output of the previous phase (technical specifications/architecture documents/code/test reports).
3. **Parallel Optimization**: S3 (Backend + Frontend) two sub-agents execute in parallel.
4. **Lightweight Scheduling**: For simple tasks (<100 lines of code, single file), S6 (Documentation) can be skipped; the PM writes a brief README directly.
5. **Failure Handling**: If any sub-agent returns empty or clearly incomplete output, retry once. If it still fails, skip that phase and note it in the final delivery.
6. **Artifact Management**: Each phase's output is written into the `{workspace}/<project-name>/` directory. All code files are organized under this directory.

### Sub-Agent Scheduling

All sub-agents are invoked using `sessions_spawn` with parameters:
- `runtime`: `"subagent"`
- `mode`: `"run"` (one-shot execution)
- `cleanup`: `"delete"`
- `model`: Use default model (follows main session)
- `runTimeoutSeconds`: 300 (5-minute timeout)

Each sub-agent's prompt template is found in `references/<role>.md`. Replace the `{...}` placeholders in the template when invoking.

### Parallel Strategy

In the S3 phase, backend and frontend sub-agents are spawned **simultaneously**. After both complete, merge the code and proceed to S4.

```python
# Pseudocode (actual implementation uses sessions_spawn + subagents poll)
spawn(backend_dev, context={spec, arch, task: "backend"})
spawn(frontend_dev, context={spec, arch, task: "frontend"})
# Wait for both sub-agents to complete
```

## Phase Details

### S1: Requirements Analysis

**Input**: User's original requirements
**Action**: Read `references/requirements-analyst.md`, replace placeholders, then spawn sub-agent
**Output**: Technical specification document → Save as `<project>/SPEC.md`
**Deliverables Include**:
- Feature list (prioritized)
- User stories / Use cases
- Non-functional requirements (performance, security, compatibility)
- Data model overview
- Acceptance criteria

### S2: Architecture Design

**Input**: SPEC.md produced in S1
**Action**: Read `references/architect.md`, pass in SPEC content, then spawn sub-agent
**Output**: Architecture design document → Save as `<project>/ARCH.md`
**Deliverables Include**:
- Tech stack selection (language, framework, libraries)
- Project directory structure
- Component tree / Module breakdown
- Data flow design
- Route design (if applicable)
- API design (if applicable)

### S3: Parallel Development

**Input**: S1 SPEC.md + S2 ARCH.md
**Action**: Spawn backend and frontend sub-agents in parallel

**Backend Development**: Read `references/backend-developer.md`, pass in SPEC + ARCH + task="backend"
**Output**: All backend code files written to `<project>/`

**Frontend Development**: Read `references/frontend-developer.md`, pass in SPEC + ARCH + task="frontend"
**Output**: All frontend code files written to `<project>/`

For pure backend projects, only spawn the backend; for pure frontend projects, only spawn the frontend.

### S4: Testing

**Input**: S1 SPEC.md + S2 ARCH.md + list of all code file paths
**Action**: Read `references/qa-engineer.md`, pass in context, then spawn sub-agent
**Output**: Test report → Save as `<project>/TEST_REPORT.md`
**Deliverables Include**:
- Test case list and results
- List of issues found (by severity)
- Test coverage assessment
- Recommended fixes

### S5: Code Review

**Input**: All code file contents + S4 TEST_REPORT.md
**Action**: Read `references/code-reviewer.md`, pass in context, then spawn sub-agent
**Output**: Review report → Save as `<project>/REVIEW.md`
**Deliverables Include**:
- Code standards review
- Security vulnerability scan
- Performance issue analysis
- Improvement suggestions

### S6: Documentation

**Input**: S1 SPEC + S2 ARCH + list of code file paths
**Action**: Read `references/documentation-engineer.md`, pass in context, then spawn sub-agent
**Output**: README.md + code comments → Save to `<project>/`
**Deliverables Include**:
- README.md (project introduction, installation, usage, API)
- JSDoc/Javadoc/docstring additions for key code

Note: For simple projects (<100 lines, single file), this can be skipped; the PM writes a brief README directly.

### S7: Integration & Delivery (PM/Main Agent)

**Input**: All artifacts from preceding phases
**Action**: The main agent executes this directly; no sub-agent spawn is needed
**Tasks**:
1. Check the completeness and consistency of all files
2. Fix critical bugs (P0/P1) based on the S4 test report
3. Fix critical issues based on the S5 review report
4. Verify that cross-file references are correct (import paths, etc.)
5. If an index.html exists, ensure it can be opened directly in a browser
6. Compile the delivery report

**Output**:
- Complete project code (`<project>/`)
- Delivery report (verbal summary, including: feature completion status, known issues, usage instructions)

## Quick Reference

### Trigger Conditions

Trigger conditions (any one is sufficient):
- User says "develop," "write code," "implement," "build" + feature description
- Involves multiple files, has a UI, requires testing, code volume >50 lines
- User explicitly requests high quality / review / testing / documentation
- User says "don't ask me, just give me the result"

Do not trigger (handle normally):
- Simple scripts (<30 lines, single file, no dependencies)
- Pure CLI tools (no UI)
- User only wants to see example/teaching code

### Skipping Phases

The PM may skip specific phases based on task complexity:
- **Simple tasks** (<100 lines, single file): Skip S6 Documentation, simplify S4 Testing
- **No-UI projects**: Skip Frontend Development
- **Pure frontend projects**: Skip Backend Development