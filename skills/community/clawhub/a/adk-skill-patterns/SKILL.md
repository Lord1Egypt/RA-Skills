---
name: adk-skill-patterns
description: 5 proven agent skill design patterns (Tool Wrapper, Generator, Reviewer, Inversion, Pipeline) from Google's ADK. Build reliable, composable skills with templates, decision trees, and composition guides. Stop cramming logic into prompts—use structured patterns instead.
metadata:
  openclaw:
    emoji: 🧩
  version: 1.0.0
---

# ADK Skill Patterns 🧩

**Source:** Google Cloud Tech — 5 Agent Skill Design Patterns  
**Adapted for:** OpenClaw Agent System  
**Purpose:** Build reliable, composable agent skills using proven architectural patterns

---

## Overview

The specification explains how to package a skill, but offers zero guidance on how to structure the logic inside it. These 5 patterns solve that problem.

| Pattern | Question It Answers | Use When |
|---------|---------------------|----------|
| **Tool Wrapper** | "How do I make my agent an expert on a specific library?" | Agent needs deep, contextual knowledge about a technology |
| **Generator** | "How do I enforce consistent output structure?" | Output format must be predictable every time |
| **Reviewer** | "How do I separate what to check from how to check it?" | Code review, quality gates, compliance checking |
| **Inversion** | "How do I stop the agent from guessing and gather requirements first?" | Complex tasks requiring full context before execution |
| **Pipeline** | "How do I enforce a strict multi-step workflow?" | Multi-phase tasks with checkpoints and approvals |

---

## Pattern 1: Tool Wrapper

**Purpose:** Give your agent on-demand context for a specific library/framework.

**Mechanism:**
- Listens for library keywords in prompts
- Dynamically loads documentation from `references/`
- Applies conventions as absolute truth only when needed

**Example Use Cases:**
- FastAPI conventions
- Internal coding standards
- Framework-specific best practices
- API design guidelines

**Template:** See `templates/tool-wrapper-SKILL.md`

---

## Pattern 2: Generator

**Purpose:** Enforce consistent output via fill-in-the-blank orchestration.

**Mechanism:**
- `assets/` holds output template
- `references/` holds style guide
- Instructions act as project manager
- Asks for missing variables before generating

**Example Use Cases:**
- API documentation generation
- Standardized commit messages
- Project scaffolding
- Technical reports

**Template:** See `templates/generator-SKILL.md`

---

## Pattern 3: Reviewer

**Purpose:** Separate review criteria from review execution.

**Mechanism:**
- Stores modular rubric in `references/review-checklist.md`
- Methodically scores submissions
- Groups findings by severity
- Swap checklist = completely different audit

**Example Use Cases:**
- PR review automation
- Security vulnerability scanning
- Code quality audits
- Compliance checking

**Template:** See `templates/reviewer-SKILL.md`

---

## Pattern 4: Inversion

**Purpose:** Stop agents from guessing — make them interview first.

**Mechanism:**
- Agent acts as interviewer, not executor
- Structured questions in phases
- Hard gates prevent premature synthesis
- User drives through answers, not prompts

**Example Use Cases:**
- Project planning/requirements gathering
- System design interviews
- Complex task specification
- Knowledge extraction

**Template:** See `templates/inversion-SKILL.md`

---

## Pattern 5: Pipeline

**Purpose:** Enforce strict sequential workflow with hard checkpoints.

**Mechanism:**
- Instructions = workflow definition
- Diamond gate conditions (user approval required)
- Cannot bypass steps or present unvalidated results
- Progressive disclosure keeps context clean

**Example Use Cases:**
- Documentation generation workflows
- Multi-step code generation
- Complex build/deploy pipelines
- Research synthesis workflows

**Template:** See `templates/pipeline-SKILL.md`

---

## Decision Tree

```
START: What does your skill need to do?
│
├─→ Provide deep knowledge about a specific library/framework?
│   └─→ Use: TOOL WRAPPER
│
├─→ Produce consistent, templated output?
│   └─→ Use: GENERATOR
│
├─→ Check/audit something against criteria?
│   └─→ Use: REVIEWER
│
├─→ Gather requirements before acting?
│   └─→ Use: INVERSION
│
├─→ Execute strict multi-step workflow?
│   └─→ Use: PIPELINE
│
└─→ Multiple of the above?
    └─→ Patterns COMPOSE (see below)
```

---

## Pattern Composition

These patterns are **not mutually exclusive** — they compose:

| Combination | Effect |
|-------------|--------|
| Pipeline + Reviewer | Multi-step workflow with quality gate at the end |
| Generator + Inversion | Gather variables via interview, then fill template |
| Pipeline + Tool Wrapper | Each step loads specific expertise as needed |
| Reviewer + Generator | Review output before generating final document |

**Principle:** Your agent only spends context tokens on the exact patterns it needs at runtime.

---

## Quick Reference: Pattern Selection

| Scenario | Pattern | Why |
|----------|---------|-----|
| "Teach my agent FastAPI conventions" | Tool Wrapper | Context loads only when FastAPI mentioned |
| "Generate consistent API docs" | Generator | Template + style guide = predictable output |
| "Automate PR reviews" | Reviewer | Swap checklist for different audit types |
| "Plan a new project" | Inversion | Gathers full requirements before designing |
| "Generate docs from code" | Pipeline | Parse → Generate → Review → Assemble |

---

## Directory Structure

```
skills/
└── your-skill/
    ├── SKILL.md              # Instructions (implements pattern)
    ├── references/           # Knowledge, checklists, style guides
    │   ├── conventions.md
    │   ├── review-checklist.md
    │   └── style-guide.md
    └── assets/               # Templates, examples
        ├── report-template.md
        └── plan-template.md
```

---

## Anti-Patterns to Avoid

❌ **Cramming everything into system prompt** — Use Tool Wrapper instead  
❌ **Different output every run** — Use Generator for consistency  
❌ **Hardcoded review criteria** — Use Reviewer for modularity  
❌ **Agent assumes context** — Use Inversion to gather requirements  
❌ **Skipped steps in workflows** — Use Pipeline for enforcement

---

## Implementation Notes for OpenClaw

1. **File Loading:** Use `read` tool to load references/assets dynamically
2. **Pattern Detection:** Check user's intent to determine which pattern to apply
3. **Composition:** Chain skills via `sessions_spawn` for complex workflows
4. **Gates:** Explicit user confirmation before proceeding (especially Pipeline/Inversion)

---

## Using This Skill

### To Apply a Pattern
Ask me: "Use the [pattern-name] pattern to [task]"

Examples:
- "Use the Tool Wrapper pattern to create a FastAPI expert skill"
- "Use the Generator pattern to standardize my report outputs"
- "Use the Reviewer pattern to build a code quality checker"
- "Use the Inversion pattern to plan my new project"
- "Use the Pipeline pattern to create a documentation workflow"

### To Get Pattern Advice
Ask: "Which pattern should I use for [scenario]?"

### To Compose Patterns
Ask: "How do I combine [pattern-1] and [pattern-2]?"

---

**Source Article:** https://x.com/GoogleCloudTech/status/2033953579824758855  
**Last Updated:** March 29, 2026
