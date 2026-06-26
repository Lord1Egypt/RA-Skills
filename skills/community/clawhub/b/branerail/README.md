# Branerail Skill: CTO-Level Architectural Agent

A production-grade skill for Claude Code that enforces CTO-level thinking in AI-native development. This skill moves beyond code generation to **architectural design, resilience patterns, and systems thinking**.

---

## What This Skill Does

**Branerail** is triggered whenever you're building, reviewing, or thinking about complex systems. It:

1. **Forces design-first thinking** before code generation
2. **Audits AI-generated code** for architectural soundness
3. **Integrates Google's design.md standard** for consistent visual design systems
4. **Guides resilience patterns** (retry, circuit breaker, bulkhead isolation)
5. **Clarifies state ownership, observability, and dependencies**
6. **Provides actionable checklists** for code review and deployment

---

## When to Use (Trigger Keywords)

Use this skill on **any conversation involving**:

- architecture, design, system design, blueprint, plan
- scale, scaling, growth, bottleneck, performance
- failure, resilience, fault tolerance, crash, disaster
- state, stateful, state management, consistency, sync
- blast radius, cascade, coupling, tight coupling, loose coupling
- data flow, data consistency, eventual consistency
- refactor, rewrite, migration, monolith, microservices
- observability, monitoring, logging, alerting, tracing, metrics
- optimize, performance, latency, throughput, bottleneck
- dependency, dependent, independent, circular dependency
- concurrency, race condition, deadlock, locking, atomicity
- distributed, consensus, replication, quorum, split brain
- single point of failure, SPOF, redundancy, failover
- contract, interface, API, versioning, backward compatibility
- DESIGN.md, design system, design tokens, visual identity
- code review, audit, architectural review, CTO-level thinking
- Claude Code, code generation, AI-generated code quality

---

## Core Philosophy: The Three Pillars

Before shipping any system, answer these three questions with certainty:

### 1. **Where Does State Live?**
What is the single source of truth for each piece of mutable data?

- Prevents race conditions and data corruption
- Ensures consistency across replicas
- Makes rollback and recovery possible

### 2. **Where Does Feedback Live?**
How do you know if the system is working? What tells you when it's failing?

- Structured logging with context
- Metrics (latency, error rate, throughput)
- Alerts for SLO violations
- Queryable, actionable traces

### 3. **What Breaks If I Delete This?**
Can you trace the blast radius of every component?

- Identifies single points of failure
- Reveals hidden dependencies
- Guides fallback strategies
- Prevents cascading failures

---

## Skill Structure

```
Branerail_skill/
├── SKILL.md                          # Main skill (27KB, comprehensive)
├── references/
│   ├── spec_template.md             # Architectural specification template
│   ├── DESIGN_template.md           # Visual design system template (DESIGN.md)
│   └── code_review_checklist.md     # Code audit checklist for Claude Code
└── README.md                        # This file
```

### SKILL.md (Main Content)
**Size**: ~27KB
**Sections**:
1. The Three Pillars (state, feedback, blast radius)
2. The Design Process Before Code (sketch, spec, deletion test, reimplementation)
3. AI as a Probabilistic Collaborator (why you need to audit)
4. Code Review Checklist (9 sections, ~100 items)
5. Architectural Anti-Patterns (what not to do)
6. Full Development Workflow (pre-code, generation, review, deployment)
7. Concurrency and Distributed Systems
8. Claude Code Integration Workflow
9. Evaluation Rubric

### references/spec_template.md
**Purpose**: Template for writing architectural specifications before coding

**Includes**:
- Component overview
- Data model (inputs, outputs)
- State and ownership matrix
- Critical paths and performance targets
- Failure modes and recovery strategy
- Observability plan (logging, metrics, alerts)
- Dependencies (internal and external)
- Testing strategy
- Scaling plan
- Security requirements
- Sign-off checklist

### references/DESIGN_template.md
**Purpose**: Google's DESIGN.md format for visual design system consistency

**Includes**:
- Color palette with semantic roles
- Typography scale (headings, body, labels, monospace)
- Spacing system (8px base units)
- Border radius conventions
- Shadow levels (elevation)
- Component patterns (buttons, inputs, cards, forms, modals)
- Responsive design breakpoints
- WCAG AA accessibility compliance
- Implementation guidelines (CSS variables, Tailwind, W3C DTCG)

**Why DESIGN.md**:
- DESIGN.md is a file format designed to describe an entire design system to AI agents, allowing any tool or model to read that file and generate interfaces that respect your brand without needing to explain it every time
- Validates against WCAG contrast ratios automatically
- Exports to Tailwind CSS, W3C Design Token Format
- Works across Claude Code, Cursor, GitHub Copilot

### references/code_review_checklist.md
**Purpose**: Comprehensive checklist for auditing AI-generated code

**Sections**:
1. Three Pillars (quick 3-minute check)
2. Spec Compliance (does code match the spec?)
3. State and Data Ownership (single source of truth?)
4. Error Handling and Resilience (handles failures?)
5. Observability (can you see what's happening?)
6. Dependencies and Coupling (what is this coupled to?)
7. Testing Coverage (happy path + failure modes?)
8. Security (no obvious holes?)
9. Performance and Scaling (will it scale?)

**Usage**: Run through this checklist when reviewing code generated by Claude Code.

---

## How to Use This Skill

### Scenario 1: Design Before Building

```
You: "I need to build a checkout system. Where should I start?"

Claude (with Branerail): 
1. Design before you code: "Sketch the architecture (boxes and arrows)"
2. Answer the three pillars
3. Write a spec (use references/spec_template.md)
4. Then ask Claude Code to generate code based on the spec
```

### Scenario 2: Code Review

```
You: [Paste AI-generated code]
You: "Is this architecturally sound?"

Claude (with Branerail):
Runs through code_review_checklist.md:
- Spec compliance? ✓
- State ownership clear? ✗ [Issue found]
- Error handling? ✓
- Observability? ✓
- [Returns detailed audit with issues and fixes]
```

### Scenario 3: Resilience Analysis

```
You: "We have user service → order service → payment gateway.
      What happens if payment gateway goes down?"

Claude (with Branerail):
1. Analyzes blast radius
2. Identifies cascade failures
3. Suggests patterns (circuit breaker, queue, retry)
4. Provides implementation guidance
```

### Scenario 4: Design System Definition

```
You: "Create our DESIGN.md to ensure all UI is on-brand"

Claude (with Branerail):
1. References DESIGN_template.md
2. Asks about brand colors, typography, components
3. Generates DESIGN.md with tokens and validation
4. Provides CLI commands to lint and export
```

---

## Integration with Claude Code

### Step 1: Reference the Skill in Your CLAUDE.md

```markdown
# CLAUDE.md - Instructions for Claude Code

You are a CTO-level code generator with Branerail guidance.

When building new features:
1. Reference the architectural spec at /specs/[feature].md
2. Use the Branerail skill to audit your code
3. Verify the Three Pillars are answered
4. Include structured logging and metrics
5. Handle all failure modes listed in the spec

When building UI:
1. Reference /DESIGN.md for colors, typography, components
2. Ensure WCAG AA contrast ratios
3. Use design tokens consistently
4. Validate with: npx @google/design.md lint DESIGN.md
```

### Step 2: Create Specs Before Coding

Use `references/spec_template.md` to create architectural specs for each major component.

### Step 3: Create DESIGN.md

Use `references/DESIGN_template.md` to define your visual design system. Export tokens to Tailwind.

### Step 4: Review Generated Code

Use `references/code_review_checklist.md` to audit code from Claude Code before merging.

---

## Key Patterns from the Skill

### Pattern 1: Write-Through Cache (Consistency)
```
Write to DB first → Update cache → Return result
(Ensures cache never has newer data than DB)
```

### Pattern 2: Circuit Breaker (Resilience)
```
External service fails 5x in a row
→ Circuit opens
→ Fail fast (don't retry)
→ After 60 seconds, try again (half-open)
→ If success, close circuit
```

### Pattern 3: Event Sourcing (Auditability)
```
Don't store state; store events
→ Event: "Order created"
→ Event: "Payment charged"
→ Event: "Order shipped"
→ Replay events to reconstruct state
```

### Pattern 4: CQRS (Scale)
```
Separate read model from write model
→ Writes go to write DB (optimized for transactions)
→ Reads go to read DB (optimized for queries)
→ Eventual consistency between them
```

---

## Real-World Example: Order Processing System

**Scenario**: Build a checkout system that handles 1000 orders/sec, resilient to payment gateway failures.

**Using Branerail**:

1. **Design Phase**
   - Sketch architecture: Web → Order Service → Payment Service → Payment Gateway
   - Answer Three Pillars:
     - **State**: Order Service owns order status (DB); Payment Service owns receipt
     - **Feedback**: Log every operation; alert on payment error rate > 5%
     - **Blast Radius**: If Payment Gateway ↓, queue and retry; orders still process
   - Write spec (references/spec_template.md)

2. **Spec Contents**
   ```markdown
   # Order Processing Spec
   
   ## Inputs
   - User ID, product IDs, amounts, currency
   
   ## Outputs
   - Order ID, status (pending/completed/failed), confirmation
   
   ## State Ownership
   - Order Service: order status (DB)
   - Payment Service: payment receipt (DB)
   
   ## Failure Modes
   - Payment timeout: Retry 3x with exponential backoff
   - Payment rejected: Alert user, order stays pending
   - Database down: Circuit breaker, fail fast
   ```

3. **Code Generation (Claude Code)**
   ```
   Prompt: "Implement order processing per /specs/orders.md
   - Handle all failure modes
   - Log every operation with orderId, status, latency
   - Emit metrics: order count, payment latency p50/p95/p99, error rate
   - Add circuit breaker for payment gateway
   - Validate against DESIGN.md for UI"
   ```

4. **Code Review (Checklist)**
   - ✓ Spec compliance (all requirements met)
   - ✓ State ownership (single source of truth)
   - ✓ Error handling (retry, circuit breaker)
   - ✓ Observability (logs, metrics, traces)
   - ✓ Tests (happy path + failure modes)
   - ✓ Performance (p99 < 2s, handles 1000/sec)

5. **Deployment**
   - Alerts fire on error rate > 5% or latency > 10s
   - Logs queryable: find orders by status, latency, errors
   - Metrics dashboard shows order throughput and error rate

---

## Checklist: Is Your System Sound?

After using this skill, score yourself:

| Criterion | Score |
|-----------|-------|
| State ownership is clear (single source of truth) | 0–3 |
| Observability is sufficient (logs, metrics, tracing) | 0–3 |
| Failure handling covers all modes (spec + extras) | 0–3 |
| Dependencies are explicit and documented | 0–3 |
| Blast radius is understood (no surprises) | 0–3 |
| Code is tested (happy path + failure modes) | 0–3 |
| Performance targets are met or on-track | 0–3 |
| Security is defensible (no obvious holes) | 0–3 |

**Target**: 2+ on all dimensions. Anything < 2 is a risk.

---

## Quick Reference: The Three Pillars Checklist

### ✓ Pillar 1: State
- [ ] Single owner for each data type
- [ ] Non-owners read from owner
- [ ] Replicas are explicit and versioned
- [ ] Conflicts are resolved deterministically
- [ ] Schema changes are migrations

### ✓ Pillar 2: Feedback
- [ ] Every critical operation is logged
- [ ] Logs are structured (JSON, key-value)
- [ ] Metrics are emitted (latency, errors, throughput)
- [ ] Alerts are defined for SLO violations
- [ ] You can reconstruct a failure from logs

### ✓ Pillar 3: Blast Radius
- [ ] Dependencies are explicit
- [ ] No circular dependencies
- [ ] Fallbacks exist for external services
- [ ] Cascade failures are prevented
- [ ] You can mentally trace impact

**If you answer YES to all 15, your system is sound.**

---

## Commands and Tools

### Google's DESIGN.md CLI

```bash
# Validate DESIGN.md against spec
npx @google/design.md lint DESIGN.md

# Check WCAG contrast ratios
npx @google/design.md lint DESIGN.md --wcag

# Compare two versions
npx @google/design.md diff DESIGN.md DESIGN-v2.md

# Export to Tailwind
npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json

# Export to W3C DTCG
npx @google/design.md export --format dtcg DESIGN.md > tokens.json
```

### Recommended Tools

- **Spec writing**: Markdown + GitHub (version control)
- **Architecture diagramming**: Excalidraw, Miro, or ASCII art
- **Code review**: GitHub PRs with checklist
- **Logging**: Structured JSON (ELK, Datadog, Grafana Loki)
- **Metrics**: Prometheus, Grafana
- **Tracing**: Jaeger, DataDog APM
- **Load testing**: k6, JMeter

---

## References

- **Branerail Skill SKILL.md**: Main guidance (27KB)
- **Spec Template**: /references/spec_template.md
- **DESIGN.md Template**: /references/DESIGN_template.md (Google's standard)
- **Code Review Checklist**: /references/code_review_checklist.md
- **Google DESIGN.md Spec**: https://github.com/google-labs-code/design.md
- **WCAG 2.1**: https://www.w3.org/WAI/WCAG21/quickref/
- **Distributed Systems**: "Designing Data-Intensive Applications" by Martin Kleppmann

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-27 | Initial release. Complete skill with bundled templates and checklists. Integrated Google's design.md standard. CTO-level guidance for Claude Code integration. |

---

## Contact & Feedback

This skill is designed for builders who refuse to let their judgment atrophy. Use it to think deeply before coding. Use it to audit AI-generated code. Use it to build resilient systems that scale.

Questions? Feedback? Open an issue or PR on the skill repository.

---

**Summary**: Branerail is your CTO-level guide in an AI-native world. It moves you from "coding faster" to "architecting better." Use it to build systems that are resilient, observable, maintainable, and right.
