---
name: feature-modification-workflow
description: A structured workflow for modifying existing features. TRIGGER when: user says "I want to change a feature", "optimize xxx", "check if xxx has room for improvement", "fix a bug", or any request involving feature modifications. Choose the appropriate workflow based on scenario complexity: simple issues go straight to code, complex issues follow the full process.
---

# Feature Modification Workflow

A standardized workflow for modifying existing features, ensuring changes are well-founded, controlled, and incremental.

## Core Principles

**Understand First, Then Modify** — Before any feature change, understand the relevant code to ensure the change direction is correct.

**Choose Workflow by Scenario** — Simple issues get simplified workflow, complex issues get full workflow. No unnecessary overhead.

**Check Docs When Needed** — Only check latest documentation when dealing with complex technical details or specific API usage. Simple changes don't need this.

**Conservative Optimization** — Optimize without changing existing flows and core logic. Avoid high-risk large-scale refactoring.

**Confirm Before Execute** — Complex changes require user confirmation before development begins.

---

## Step 1: Determine Scenario

After receiving a user request, **first determine which scenario it falls into**, then choose the corresponding workflow:

| Scenario | Characteristics | Workflow |
|----------|-----------------|----------|
| **Simple Issue** | Change color, text, spacing, config values | Simplified: Read code → Change directly |
| **Bug Fix** | Fix errors, exceptions, unexpected behavior | Must analyze cause. Simple bugs use simplified workflow, complex bugs use full workflow |
| **Complex Issue** | New features, logic optimization, multi-file changes, architecture involved | Full 5-step workflow |
| **Refactoring** | Core flow changes, large-scale code adjustments | Full 5-step workflow |

---

## Scenario 1: Simple Issue (Simplified Workflow)

### What Counts as Simple Issue

- UI adjustments: change color, font size, spacing, borders
- Text modifications: change copy, hints, labels
- Config modifications: change defaults, parameters
- Single-file small changes: doesn't affect other modules

### Simplified Workflow

```
1. Read relevant code (only the part to change)
2. Make the change
3. Inform user it's done
```

### Example

**User**: Change the login button color to blue

**AI**:
- Read button code → Find color setting → Change to blue → Done

---

## Scenario 2: Bug Fix (Must Analyze Cause)

### Core Requirement

**Bug fixes must first locate the cause**. Don't change code based on guessing.

### Simple Bug (Simplified Workflow)

**Characteristics**: Cause is clear, small change scope, doesn't affect other features

```
1. Analyze current state: locate bug cause
2. Fix directly
3. Inform user it's done
```

### Complex Bug (Full Workflow)

**Characteristics**: Cause unclear, involves multiple modules, may affect other features, requires architecture changes

```
Follow the full 5-step workflow
```

### Judgment Criteria

| Simple Bug | Complex Bug |
|------------|-------------|
| Clear error message, can locate directly | Cause unclear, needs investigation |
| Small change scope, 1-2 places | Involves multiple files/modules |
| Doesn't affect other features | May cause chain reactions |
| Doesn't involve core logic | Needs to change core flow |

---

## Scenario 3: Complex Issue (Full 5-Step Workflow)

### What Counts as Complex Issue

- Adding new features
- Optimizing logic/performance
- Changes involving multiple files
- Architecture adjustments
- Requires design proposals

### Full Workflow

#### Step 1: Understand the Project Globally

After receiving a feature change request, **don't start coding directly**. First do the following:

1. **Understand project structure**
   - Use Glob to view directory structure
   - Identify core modules and dependencies
   - Find relevant config files, entry files

2. **Read key files**
   - Project documentation (CLAUDE.md, README.md, etc.)
   - Core module implementation files
   - Files directly related to the change target

3. **Understand existing flows**
   - How data flows
   - How modules communicate
   - What the user interaction flow is

**Output Format**:
```
## Project Overview
- Project type: xxx
- Core modules: xxx, xxx, xxx
- Data flow: xxx → xxx → xxx

## Related Modules
- Module A: responsible for xxx
- Module B: responsible for xxx
- Dependencies: A → B → C
```

#### Step 2: Analyze Current State

After understanding the project, analyze the current state of the change target:

1. **Current implementation analysis**
   - How is current code implemented
   - What technologies/patterns are used
   - What key design decisions were made

2. **Identify strengths**
   - What's good about current implementation
   - Which designs are reasonable and worth keeping

3. **Identify bottlenecks**
   - Where are performance bottlenecks
   - Where are UX bottlenecks
   - Where are maintainability bottlenecks

4. **Identify weaknesses**
   - Code quality issues
   - Design flaws
   - Extensibility limitations

**Output Format**:
```
## Current State Analysis

### Current Implementation
[Describe current implementation]

### Strengths
- xxx
- xxx

### Bottlenecks/Weaknesses
- xxx: [specific description]
- xxx: [specific description]
```

#### Step 3: Propose Optimization Plan

Based on analysis, propose optimization plan. **Key constraint: don't change existing flow**

- Optimization should be incremental, not a rewrite
- Keep core logic and data flow
- Only make local improvements

**Output Format**:
```
## Optimization Plan

### Overview
[Briefly describe optimization approach]

### Optimization Points
1. xxx: [specific change, expected effect]
2. xxx: [specific change, expected effect]

### What Not to Change
- xxx: [why to keep]

### Risk Assessment
- Change scope: [large/medium/small]
- Affected modules: xxx, xxx
- Note: xxx
```

#### Step 4: List Plan and Ask User

Break down the optimization plan into specific steps, list the plan and ask user for confirmation:

**Output Format**:
```
## Development Plan

### Step List
1. [ ] Step 1: xxx
2. [ ] Step 2: xxx
3. [ ] Step 3: xxx

### Confirmation Questions
- Does the above plan meet your expectations?
- Any steps need adjustment or addition?
- Can I start execution?
```

**Wait for user response**. Don't start development on your own.

#### Step 5: Execute Step by Step After Confirmation

After user confirms:

1. Use TodoWrite to create task list, track progress
2. Develop step by step
3. Mark completion and inform user after each step
4. Report issues promptly, don't bypass problems

**During development**:
- Keep communication, ask user for important decisions
- Complete one step before starting next
- If plan needs adjustment, ask user first

---

## Scenario 4: Refactoring (Full 5-Step Workflow)

Refactoring must follow the full workflow because of high risk and large impact scope.

**Characteristics of refactoring**:
- Changes to core flow
- Large-scale code adjustments
- Involves multiple modules
- May affect existing features

---

## Conditional Step: Check Documentation

**Not all changes need documentation check**. Only check in these cases:

### When to Check Documentation

1. **Complex technical details**
   - Audio processing algorithms (sample rate conversion, silence detection)
   - Network protocol details (WebSocket frame format, Protobuf encoding)
   - Multi-threading/concurrency issues (thread safety, lock mechanisms)

2. **Unsure about specific API usage**
   - Framework API parameter meaning unclear
   - Library function best practices
   - API changes after version updates

3. **Involves specifications or standards**
   - Data format specifications
   - Protocol standard documents
   - Security/compliance requirements

### When NOT to Check Documentation

- UI layout adjustments (spacing, colors, fonts)
- Simple logic changes (conditionals, parameter adjustments)
- Already familiar API usage
- Similar implementation exists in project for reference

### Documentation Check Tools Priority

1. **Context7** (`mcp__context7__resolve-library-id` + `mcp__context7__query-docs`)
   - Latest docs for programming libraries/frameworks
   - PySide6, React, numpy, etc.

2. **WebSearch**
   - Protocol specifications, technical articles
   - WebSocket protocol, best practice articles

---

## Quick Reference

### Scenario-Workflow Mapping

| Scenario | Workflow |
|----------|----------|
| Simple Issue | Read code → Change directly |
| Simple Bug | Analyze cause → Fix directly |
| Complex Bug | Full 5 steps |
| Complex Issue | Full 5 steps |
| Refactoring | Full 5 steps |

### Full 5 Steps

| Step | Action | Output |
|------|--------|--------|
| 1 | Understand globally | Project overview |
| 2 | Analyze current state | Strengths/bottlenecks/weaknesses |
| 3 | Propose plan | Optimization points/what not to change |
| 4 | List plan and ask | Step list + confirmation questions |
| 5 | Execute after confirmation | Develop step by step |

**Conditional**: Check documentation (for complex technical issues)

---

Remember: **Determine scenario first, then choose workflow**. Handle simple issues simply, plan complex issues carefully.