---
name: coding-contract
description: >
  Generate language-agnostic coding contracts (spec.md) from requirements.
  Outputs interface signatures, behavioral constraints, and verification
  checklists — never implementation code. Designed for the "strong model
  writes spec, weak model writes code" workflow. Spec files are reusable
  knowledge artifacts: write once, implement in any language. Use when
  the user wants to create a coding spec, define interfaces before
  implementation, or build a reusable engineering contract. Triggers on:
  "写规范", "生成 spec", "定义接口", "做实现蓝图", "coding contract",
  "implementation spec", "technical specification", or when a brainstorming
  design document needs to be converted into an actionable engineering plan.
---

# Coding Contract Generator

Generate coding contracts that capture engineering knowledge as persistent,
language-agnostic artifacts. A contract defines WHAT to build and WHAT
CONSTRAINTS to respect, but never HOW to implement it. Any developer or
AI agent, in any language, can implement the same contract and produce
functionally equivalent code.

Produce spec.md files containing interface definitions, behavioral
constraints, and verification checklists — never complete implementations.

## Core Principles

### Iron Rules (Non-Negotiable)

1. **NO COMPLETE CODE**: Output interface signatures and pseudocode only.
   Never write function bodies, class implementations, configuration files,
   or executable scripts. The implementer writes the code; you write the contract.

2. **CONSTRAINTS ARE MANDATORY**: Every spec MUST include a Constraint Layer
   (Section 4). If you think "this is obvious", write it anyway. The
   implementer may not share your assumptions.

3. **EVERY INTERFACE MUST HAVE TESTS**: For each public function in Section 3,
   at least one test case MUST exist in Section 5. Untested interfaces are
   unspecified interfaces.

4. **NO HARDCODED MAGIC VALUES**: Use descriptive placeholders
   (e.g., `[TIMEOUT_MS]`, `[MAX_RETRY_COUNT]`) or explain where the value
   comes from (e.g., "configured via environment variable"). Never embed
   literal numbers without context.

5. **SELF-VALIDATE BEFORE OUTPUT**: After drafting the spec, check against
   the Self-Validation Checklist below. Fix gaps before presenting.

6. **LANGUAGE-AGNOSTIC**: This skill works for any software domain — mobile,
  backend, frontend, embedded, ML, data pipelines. Do not assume a specific
  tech stack unless the user provides one.

## Workflow

### Phase 1: Requirement Ingestion

Determine the input mode:

**Mode A — Brainstorming Document Available:**

If the user provides a design document from a brainstorming session, read it
carefully. Extract: feature scope, module boundaries, tech stack preferences,
data models, and user-approved decisions. Proceed to Phase 2.

**Mode B — Raw Requirement (No Prior Design):**

If the user provides only a natural language description, conduct a structured
clarification dialog. Ask as many questions as needed — there is no limit.
Goal: resolve all ambiguity before writing a single line of spec.

Clarification topics to cover (ask selectively based on context):

- **Scope**: What is in-scope vs. out-of-scope for this feature?
- **Users/API Consumers**: Who calls this code? Human users, internal services,
  external API clients?
- **Tech Stack**: Any language, framework, or library constraints?
- **Existing Codebase**: Are we extending existing modules or creating new ones?
- **Quality Requirements**: Performance targets, availability SLAs, security
  compliance needs?
- **Failure Expectations**: What happens when things go wrong? Crash, degrade,
  retry, notify?
- **Data & State**: Persistent storage? Caching? Real-time or batch?
- **Integration Points**: External APIs, message queues, third-party services?
- **Non-Functional**: Concurrency model, deployment constraints, regulatory
  requirements?

Continue asking until the user confirms the picture is complete. Better to
over-communicate than to guess.

### Phase 2: Context Analysis

Read relevant existing code if available:

- Identify current architecture patterns (layered, hexagonal, microservices, etc.)
- Note existing conventions for naming, error handling, and module organization
- Mark integration points where new code must connect to old code
- Respect existing conventions; do not introduce foreign patterns unless
  explicitly requested

If no existing codebase (greenfield), establish default conventions based on
industry best practices for the chosen tech stack. Document these decisions in
Section 6.

### Phase 3: Spec Generation

Write the spec following the structure in `references/spec-template.md`.
Key generation rules:

- **Section 1 (Overview)**: One-paragraph goal. Explicit scope boundaries with
  "IN: ... OUT: ..." format.

- **Section 2 (Module Structure)**: Directory tree (max 3 levels). Each module
  gets a one-sentence responsibility description. Arrows show dependencies.

- **Section 3 (Interface Definitions)**: 
  - Public function signatures with input/output types
  - Data class fields with types and semantic meaning
  - Thrown exceptions and their conditions
  - Pseudocode only — `// implementation left to implementer`
  - Group by module

- **Section 4 (Constraint Layer)** — NEVER skip:
  - Performance (latency, throughput, memory, cpu)
  - Degradation strategies for each external dependency
  - Boundary conditions (empty input, null, max size, concurrency)
  - Threading model (what runs where, synchronization)
  - Security (auth, encryption, input validation, secrets handling)
  - Refer to `references/constraint-patterns.md` for common patterns.

- **Section 5 (Verification Checklist)**:
  - Unit tests: input → expected output, including error cases
  - Integration tests: multi-component scenarios
  - Performance tests: measurable benchmarks
  - Use checkboxes (`- [ ]`) for trackability

- **Section 6 (Decisions)**:
  - Architecture choices with rationale
  - Trade-offs made (what was sacrificed and why)
  - Explicit user approvals on contentious decisions

### Phase 4: Self-Validation

Before output, verify:

- [ ] Every public function in Section 3 has at least one test in Section 5
- [ ] Section 4 (Constraint Layer) is non-empty
- [ ] No executable code appears in the spec (only signatures and pseudocode)
- [ ] No hardcoded magic numbers without explanation
- [ ] All external dependencies are listed with their purpose
- [ ] No ambiguous language: "appropriate", "reasonable", "etc.", "as needed"
      — replace with precise definitions
- [ ] Error cases are explicitly defined (not just "handle errors gracefully")
- [ ] Threading model is specified (what runs on main thread vs. background)

If any check fails, revise the spec and re-validate.

### Phase 5: Delivery

Output the complete spec as a file named `spec.md`. Prefix with:

```
<!-- Generated by coding-contract skill -->
<!-- This is a coding contract — interface signatures and constraints only, not implementation code -->
<!-- Implementer: fill in all [PLACEHOLDER] values before coding -->
```

Save the file. Do not proceed to implementation unless explicitly asked.

## Output Location

Default: `docs/specs/YYYY-MM-DD-<feature-name>.md`

Override: If the user specifies a location, use theirs.

## References

- **Output template**: Read `references/spec-template.md` for the complete
  spec.md format with annotated examples.
- **Constraint patterns**: Read `references/constraint-patterns.md` when writing
  Section 4 to ensure comprehensive coverage.
