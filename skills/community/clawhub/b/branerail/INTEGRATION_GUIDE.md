# SystemDesign Skill: Integration & Deployment Guide

This guide walks you through installing and using the SystemDesign skill across your Claude Code workflows.

---

## What You're Getting

**SystemDesign** is a production-grade CTO-level agent skill that:

- Forces architectural thinking before code generation
- Audits AI-generated code for soundness
- Integrates Google's DESIGN.md standard
- Provides actionable checklists and templates
- Works natively with Claude Code

**Package Contents**:
- `SKILL.md` — 726 lines of architectural guidance (main skill)
- `README.md` — Overview and usage patterns
- `spec_template.md` — Template for architectural specs
- `DESIGN_template.md` — Template for visual design systems (Google's DESIGN.md)
- `code_review_checklist.md` — Checklist for auditing AI code (594 lines)

---

## Installation

### Option 1: Install as a Custom Skill (Claude.ai / Claude Code)

1. **Download the files**: All files are in `/mnt/user-data/outputs/`

2. **Create skill directory**:
   ```bash
   mkdir -p ~/.claude/skills/systemdesign
   cp SKILL.md ~/.claude/skills/systemdesign/
   mkdir ~/.claude/skills/systemdesign/references
   cp spec_template.md DESIGN_template.md code_review_checklist.md \
     ~/.claude/skills/systemdesign/references/
   ```

3. **Reference in CLAUDE.md** (at root of your project):
   ```markdown
   # CLAUDE.md - Instructions for AI Code Generation
   
   You have access to the SystemDesign skill.
   
   When building features:
   1. Use the SystemDesign skill for architectural guidance
   2. Reference /specs/[feature].md for each component
   3. Verify the Three Pillars before shipping:
      - Where does state live?
      - Where does feedback live?
      - What breaks if I delete this?
   4. Use code_review_checklist.md to audit your output
   ```

### Option 2: Manual Integration

Just reference the files directly in your project:

```bash
# Project structure
my-project/
├── CLAUDE.md                          # Instructions for Claude Code
├── DESIGN.md                          # Your visual design system
├── specs/                             # Architectural specs
│   ├── order-processing.md
│   ├── auth-service.md
│   └── ...
├── .systemdesign/                     # References (optional)
│   ├── code_review_checklist.md
│   └── architectural_patterns.md
└── src/
```

---

## Quick Start: 3-Step Workflow

### Step 1: Design (Before Coding)

Use **spec_template.md** to write your architecture:

```bash
# Create architectural spec
cp spec_template.md specs/checkout-system.md
# Edit to fill in your component details
```

**What to define**:
- Inputs and outputs
- State ownership (where does data live?)
- Failure modes (what can go wrong?)
- Observability plan (logs, metrics, alerts)
- Dependencies and fallbacks

### Step 2: Generate (With Claude Code)

Prompt Claude Code with your spec:

```
Using the spec at /specs/checkout-system.md:

1. Implement the checkout service
2. All state mutations go through OrderService (single source of truth)
3. Handle all failure modes: timeout, invalid input, gateway down
4. Log every operation: orderId, status, latency, errors
5. Emit metrics: order count, latency p50/p95/p99, error rate
6. Add circuit breaker if payment fails >5%
7. Ensure code passes the code_review_checklist
```

### Step 3: Review (With Checklist)

Use **code_review_checklist.md** to audit generated code:

```bash
# Run through the checklist (mentally or with Claude)
# Sections to review:
# 1. Spec compliance
# 2. State and data ownership
# 3. Error handling
# 4. Observability
# 5. Dependencies
# 6. Testing
# 7. Security
# 8. Performance
# 9. The Three Pillars
```

---

## Using with DESIGN.md

### Generate Your Design System

1. **Start from template**:
   ```bash
   cp DESIGN_template.md DESIGN.md
   # Edit to define your brand colors, typography, components
   ```

2. **Validate with Google's CLI**:
   ```bash
   npx @google/design.md lint DESIGN.md
   # Checks for errors, WCAG AA contrast, token references
   ```

3. **Export tokens**:
   ```bash
   # To Tailwind CSS
   npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json
   
   # To W3C Design Token Format
   npx @google/design.md export --format dtcg DESIGN.md > tokens.json
   ```

4. **Reference in CLAUDE.md**:
   ```markdown
   When generating UI:
   1. Reference DESIGN.md for colors, typography, components
   2. Ensure all buttons use primary button pattern from DESIGN.md
   3. Check contrast ratios (WCAG AA minimum)
   4. Use design tokens consistently
   ```

---

## Trigger Keywords (When to Use This Skill)

The SystemDesign skill should trigger whenever you mention:

**Architecture & Design**:
- "architecture", "design", "system design", "blueprint"

**Performance & Scaling**:
- "scale", "scaling", "performance", "bottleneck", "latency"

**Failure & Resilience**:
- "failure", "resilience", "fault tolerance", "crash", "goes down"

**State & Consistency**:
- "state", "stateful", "state management", "consistency", "sync"

**Dependencies**:
- "dependency", "coupled", "loose coupling", "blast radius", "cascade"

**Observability**:
- "logging", "metrics", "monitoring", "alerting", "tracing"

**Code Quality**:
- "code review", "audit", "refactor", "Claude Code", "AI-generated"

---

## Real Example: Building a Payment Service

### Step 1: Write the Spec

```markdown
# Payment Service Specification

## Purpose
Reliably charge users and handle payment failures.

## Inputs
- Amount (positive decimal, 2 places)
- Currency (ISO 4217)
- User ID, Order ID

## Outputs
- Transaction ID, status (success/failed), timestamp

## State Ownership
Payment Service owns payment receipt (single source of truth in database).

## Failure Modes
| Failure | Recovery |
|---------|----------|
| Payment gateway timeout | Retry 3x with exponential backoff |
| Invalid amount | Reject immediately |
| Rate limit | Queue and retry later |
| Database down | Circuit breaker, fail fast |

## Observability
- Log: every charge attempt with amount, orderId, status
- Metrics: charge count, latency p50/p95/p99, error rate
- Alerts: error rate > 5% for 5 min, timeout rate > 1%

## Dependencies
- Payment Gateway (external): 5s timeout, retry 3x
- Database: write receipt, critical

## Questions Answered
- **State**: Payment Service owns receipt
- **Feedback**: Logs every charge; metrics on error rate
- **Blast Radius**: If gateway ↓, queue retries; orders still process
```

### Step 2: Prompt Claude Code

```
Implement payment processing per /specs/payment.md:

Checklist:
- ✓ All failure modes handled (timeout, invalid, rate limit)
- ✓ Logs structured JSON with orderId, status, latency
- ✓ Metrics emitted (count, latency, errors)
- ✓ Circuit breaker on gateway (fail fast after 5 failures)
- ✓ Idempotency key (safe to retry)
- ✓ Tests for happy path + all failure modes
- ✓ Passes code_review_checklist.md
```

### Step 3: Review with Checklist

**Three Pillars**:
- ✓ State: Payment Service is single owner of receipt
- ✓ Feedback: Logs every charge; alerts on error rate > 5%
- ✓ Blast Radius: If gateway down, queues retry; orders unaffected

**Spec Compliance**: ✓ All requirements met

**Error Handling**: ✓ Timeout, retry, circuit breaker

**Observability**: ✓ Structured logs, metrics, alerts

**Result**: ✅ **APPROVED** - Ready to deploy

---

## Integration Patterns

### Pattern 1: Monorepo with Multiple Services

```
monorepo/
├── CLAUDE.md (global rules)
├── DESIGN.md (global design system)
├── SystemDesign/
│   ├── SKILL.md
│   ├── code_review_checklist.md
│   └── templates/
├── services/
│   ├── auth/
│   │   ├── CLAUDE.md (service-specific overrides)
│   │   ├── specs/
│   │   └── src/
│   ├── orders/
│   └── payments/
```

### Pattern 2: Feature Branch Workflow

```
1. Create feature branch
2. Write spec in /specs/feature-name.md
3. Run: claude "Implement per /specs/feature-name.md"
4. Review generated code with code_review_checklist.md
5. Commit spec + code
6. PR review includes checklist verification
7. Merge and deploy
```

### Pattern 3: Code Review Automation

Add to your PR template:

```markdown
## Code Review Checklist

- [ ] Spec is written and attached
- [ ] Code passes code_review_checklist.md
- [ ] All three pillars are answered
- [ ] DESIGN.md compliance verified (if UI)
- [ ] Tests cover happy path + failure modes
- [ ] Performance targets met
- [ ] Security audit passed

**Approval**: All items checked
```

---

## Key Concepts to Internalize

### The Three Pillars

**You must be able to answer these three questions with certainty**:

1. **Where does state live?**
   - What is the single source of truth for each data type?
   - Can you name the component that owns it?
   - Do non-owners read from the owner?

2. **Where does feedback live?**
   - Can you reconstruct a failure from logs?
   - Are metrics emitted (latency, errors)?
   - Are alerts defined for SLO violations?

3. **What breaks if I delete this?**
   - What calls into this component?
   - What depends on its output?
   - Are there fallbacks for external dependencies?

**If you answer "I'm not sure" to any, the system is not ready.**

### The Design Process (Before Code)

1. **Sketch** (5 min): Draw boxes and arrows
2. **Spec** (30 min): Define inputs, outputs, failure modes
3. **Delete Test** (5 min): Trace blast radius
4. **Code** (2 hours): Prompt Claude Code with spec as constraint
5. **Review** (30 min): Run through code_review_checklist.md
6. **Deploy** (30 min): Verify monitoring, alerts, fallbacks

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Code Without Design
**Problem**: Write code first, design later. Leads to fragile, tightly coupled systems.
**Fix**: Always write spec (spec_template.md) before prompting Claude Code.

### ❌ Mistake 2: No Observability
**Problem**: Code runs silently; users discover bugs.
**Fix**: Define logging (structured JSON), metrics, and alerts in spec.

### ❌ Mistake 3: Ignored Failure Modes
**Problem**: "It works when everything is fine" — but fails when external services are down.
**Fix**: List all failure modes in spec; implement recovery for each.

### ❌ Mistake 4: Scattered State
**Problem**: Multiple components own same data; race conditions and data corruption.
**Fix**: Designate single owner for each data type in spec.

### ❌ Mistake 5: Untested Code
**Problem**: AI generates syntactically correct but logically flawed code.
**Fix**: Use code_review_checklist.md; require tests for happy path + failure modes.

### ❌ Mistake 6: Skip the Deletion Test
**Problem**: Hidden dependencies discovered too late.
**Fix**: Before shipping, mentally trace: "If I delete this component, what breaks?"

---

## Next Steps

1. **Read SKILL.md** (main guidance) — 726 lines
2. **Copy spec_template.md** to your project; fill it out
3. **Copy DESIGN_template.md** if you're building UI
4. **Reference code_review_checklist.md** when reviewing AI-generated code
5. **Add CLAUDE.md** at project root with links to these files
6. **Prompt Claude Code** with your spec as a constraint

---

## FAQ

**Q: Does this skill replace a CTO?**
A: No. It amplifies human judgment. You still decide architecture; the skill helps you think deeper and avoid common traps.

**Q: Will this slow down development?**
A: No. Writing a good spec (30 min) saves debugging (days). Design before code is faster overall.

**Q: Can I use this for small projects?**
A: Yes. Even small projects benefit from clear state ownership and observability.

**Q: What if I don't follow the spec?**
A: You can. But you'll encounter the problems the spec was designed to prevent: race conditions, cascade failures, silent errors, scalability issues.

**Q: How often should I update the spec?**
A: Once per feature. Update if you discover new failure modes or constraints.

**Q: Can I share the spec with non-technical stakeholders?**
A: Yes. The spec is human-readable and documents what the system will do and why.

---

## Support & Feedback

- Questions? Re-read SKILL.md (it answers most questions)
- Feedback? Adapt the templates to your context
- Issues? The checklist will surface them during code review

---

## Summary

**SystemDesign** is your CTO-level guide in an AI-native world.

Use it to:
- ✓ Design before you code
- ✓ Audit AI-generated code for soundness
- ✓ Understand failure modes and mitigation
- ✓ Build systems that scale, fail gracefully, and recover
- ✓ Stay in control of your architecture

**The core message**: AI generates code fast. Your job is to conduct the orchestra, not play a single instrument. Use SystemDesign to elevate your thinking.

---

**Ready to build?** Start with Step 1: Write the spec.
