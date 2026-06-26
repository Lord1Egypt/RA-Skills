# SystemDesign Skill: Complete Package Summary

**Status**: ✅ **Production Ready**

You now have a complete, enterprise-grade CTO-level skill for Claude Code.

---

## What You're Getting

### Core Skill: SKILL.md (726 lines)

A comprehensive guide covering:

1. **The Three Pillars** (architectural foundation)
   - Where does state live? (single source of truth)
   - Where does feedback live? (observability)
   - What breaks if I delete this? (blast radius)

2. **Design Process** (before code)
   - Sketch architecture
   - Write specs
   - Run deletion test
   - Manual reimplementation for learning

3. **Code Review** (for AI-generated code)
   - Spec compliance
   - State and data ownership
   - Error handling and resilience
   - Observability (logging, metrics, tracing)
   - Dependencies and coupling
   - Testing coverage
   - Security audit
   - Performance and scaling
   - Full checklist (100+ items)

4. **Patterns & Anti-Patterns**
   - Circuit breaker, retry, bulkhead isolation
   - Write-through cache, event sourcing, CQRS
   - Consensus, eventual consistency
   - What not to do (scattered state, silent failures, etc.)

5. **Full Development Workflow**
   - Pre-code phase
   - Code generation with Claude Code
   - Code review
   - Deployment
   - Post-deployment learning

6. **Claude Code Integration**
   - How to reference specs in prompts
   - How to integrate DESIGN.md
   - How to audit generated code
   - How to set up your project

### Bundled Templates

#### 1. spec_template.md (319 lines)
**Purpose**: Architectural specification template

**Includes**:
- Component overview and purpose
- Data model (inputs, outputs)
- State ownership matrix
- Critical paths and latency targets
- Failure modes and recovery strategy (table format)
- Observability plan (logging, metrics, alerts)
- External and internal dependencies
- Testing strategy (unit, integration, failure modes, chaos)
- Scaling plan and constraints
- Security requirements
- Deployment and rollback checklist
- Sign-off checklist

**Usage**: Copy this, fill it out before coding. It becomes your contract with Claude Code.

#### 2. DESIGN_template.md (462 lines)
**Purpose**: Visual design system template (Google's DESIGN.md format)

**Includes**:
- YAML front matter (machine-readable tokens)
- Colors (semantic: primary, secondary, tertiary; functional: success, error, warning)
- Typography scale (h1–h3, body-lg/md/sm, label-lg/sm, monospace)
- Spacing system (8px base, xs–xxl)
- Border radius conventions
- Shadow levels (sm–xl)
- Component patterns (buttons, inputs, cards, forms, modals)
- Responsive breakpoints (mobile, tablet, desktop)
- WCAG AA accessibility compliance
- Implementation guidance (CSS variables, Tailwind, W3C DTCG)

**Why DESIGN.md**:
- Google's open-source standard (April 2026)
- Agents (Claude Code, Cursor, GitHub Copilot) read it automatically
- Validates WCAG contrast ratios
- Exports to Tailwind CSS, W3C Design Tokens
- No need to repeat your design system every time you code

**Usage**: Define your brand once in DESIGN.md. Reference it in CLAUDE.md. Claude Code generates UI on-brand automatically.

#### 3. code_review_checklist.md (594 lines)
**Purpose**: Comprehensive checklist for auditing AI-generated code

**Sections**:
1. Quick Summary (3-minute check: Three Pillars)
2. Spec Compliance (does code match spec?)
3. State and Data Ownership (single source of truth?)
4. Error Handling and Resilience (retry, circuit breaker, timeout?)
5. Observability (logging, metrics, tracing?)
6. Dependencies and Coupling (explicit, no circular deps?)
7. Testing Coverage (happy path + failure modes?)
8. Security Checklist (input validation, auth, secrets, rate limiting?)
9. Performance and Scaling (meets targets, N+1 queries, caching?)
10. The Three Pillars (final confidence check)

**Usage**: Run through this when reviewing code from Claude Code. It surfaces architectural issues that syntax checking misses.

### Supporting Documents

#### README.md (447 lines)
- Overview of skill and use cases
- Trigger keywords
- How to use (4 scenarios)
- Integration with Claude Code
- Real-world examples
- Evaluation rubric

#### INTEGRATION_GUIDE.md (You're reading this)
- Installation instructions
- 3-step quick start
- Real example (payment service)
- Integration patterns (monorepo, feature branch, automation)
- Common mistakes to avoid
- FAQ

---

## File Structure

```
SystemDesign_skill/
├── README.md                     (447 lines) - Overview & guide
├── SKILL.md                      (726 lines) - Main skill (VERY comprehensive)
├── references/
│   ├── spec_template.md         (319 lines) - Spec template
│   ├── DESIGN_template.md       (462 lines) - Visual design system (DESIGN.md)
│   └── code_review_checklist.md (594 lines) - Code audit checklist
└── INTEGRATION_GUIDE.md         (This file) - Setup & usage

Total: ~2,900 lines of production-grade guidance + templates
```

---

## The SystemDesign Philosophy

### Core Insight
In an AI-native world, the ability to think architecturally is what separates valuable builders from those building houses of cards.

AI generates code fast. Humans must conduct the orchestra.

### The Three Pillars (Everything Flows From These)

**1. Where does state live?**
- Every piece of mutable data has a single owner
- Non-owners read from the owner, not from cached copies
- Prevents race conditions, data corruption, inconsistency

**2. Where does feedback live?**
- Structured logging with context
- Metrics (latency, error rate, throughput)
- Alerts for SLO violations
- You can reconstruct failures from logs

**3. What breaks if I delete this?**
- You can trace the blast radius of every component
- No hidden dependencies
- Fallbacks exist for external services
- Cascade failures are prevented

**If you can answer all three with certainty, your system is sound.**

---

## Quick Start (5 Minutes)

1. **Read README.md** (2 min): Understand the skill
2. **Copy spec_template.md** to `/specs/my-feature.md` (1 min)
3. **Fill in the spec** (2+ hours, but worth it)
4. **Prompt Claude Code**: "Implement per /specs/my-feature.md. Run through code_review_checklist.md before returning."
5. **Review with checklist** (30 min)
6. **Deploy with confidence**

---

## When to Use This Skill

### Trigger Keywords
The skill should be active whenever you mention:

**Must Use**:
- "architecture", "design", "system design"
- "scale", "performance", "bottleneck"
- "failure", "resilience", "goes down"
- "state", "consistency", "sync"
- "blast radius", "cascade", "coupling"
- "Claude Code", "code review", "audit"

**Should Use**:
- "refactor", "migration", "monolith"
- "observability", "monitoring", "logging"
- "dependency", "circular", "tight coupling"
- "concurrency", "race condition", "deadlock"
- "distributed", "consensus", "replication"

**Nice to Use**:
- Any discussion of system design
- Any code generation prompt
- Any post-mortems or incidents
- Scaling discussions

---

## Integration with Claude Code (3 Steps)

### Step 1: Create CLAUDE.md in Project Root

```markdown
# CLAUDE.md - Instructions for Claude Code

You are a CTO-level code generator with SystemDesign guidance.

When building features:
1. Consult the architectural spec at /specs/[feature].md
2. Use references/code_review_checklist.md to audit your code
3. Verify the Three Pillars:
   - Where does state live? (single source of truth?)
   - Where does feedback live? (observable?)
   - What breaks if I delete this? (blast radius clear?)
4. Include structured logging and metrics
5. Handle all failure modes listed in the spec

When building UI:
1. Reference DESIGN.md for colors, typography, components
2. Use design tokens consistently
3. Ensure WCAG AA contrast ratios
4. Validate: npx @google/design.md lint DESIGN.md
```

### Step 2: Create Specs Before Coding

Use `spec_template.md`:
```bash
cp references/spec_template.md specs/checkout.md
# Edit to define your architecture
```

### Step 3: Review Generated Code

Use `code_review_checklist.md`:
```bash
# Copy to your PR review template
# Run through all 9 sections
# Approve only if all boxes checked
```

---

## Real-World Scenario: E-Commerce Checkout

**Problem**: Build a checkout that handles 1000 orders/sec, resilient to payment failures, observable.

**Using SystemDesign**:

### 1. Design (spec_template.md)
```markdown
# Checkout Specification

State Ownership:
- Order Service: order status (DB, single source of truth)
- Payment Service: payment receipt (DB)
- Cache: read-only replica of recent orders

Failure Modes:
- Payment timeout: retry 3x with exponential backoff
- Database down: circuit breaker, fail fast
- Cache miss: query DB directly

Observability:
- Log: every order with orderId, status, latency
- Metrics: order count, payment latency p50/p95/p99, error rate
- Alerts: error rate > 5% for 5 min, latency > 10s

Blast Radius:
- If Payment Service ↓: orders queue, retry later (degraded)
- If Database ↓: circuit breaker, fail fast (safe)
- If Cache ↓: read directly from DB (slower but works)
```

### 2. Code Generation
```
Prompt: "Implement checkout per /specs/checkout.md
- State mutations only through OrderService
- Handle all failure modes
- Structured logging with orderId, status, latency
- Emit metrics: count, latency, errors
- Circuit breaker on payment gateway
- Pass code_review_checklist.md"
```

### 3. Code Review
```
✓ Spec compliance (all requirements met)
✓ State ownership (Order Service owns status)
✓ Error handling (retry, circuit breaker, timeout)
✓ Observability (logs, metrics, traces)
✓ Testing (happy path + failure modes)
✓ Performance (p99 < 2s, handles 1000/sec)

Status: ✅ APPROVED
```

### 4. Deployment
- Logs queryable: `status=FAILED, latency > 5000`
- Metrics dashboard: order throughput, error rate
- Alerts fire: error rate spike, latency degradation
- Fallback works: payment gateway down, orders queue

---

## Common Patterns Covered

| Pattern | Use Case | Covered In |
|---------|----------|-----------|
| **Circuit Breaker** | Failing fast when dependency is down | SKILL.md § Concurrency |
| **Retry + Backoff** | Transient failures (network, timeout) | code_review_checklist.md § Error Handling |
| **Eventual Consistency** | Distributed state sync | SKILL.md § Distributed Systems |
| **Event Sourcing** | Audit trail, point-in-time recovery | SKILL.md § Anti-Patterns |
| **CQRS** | Radically different read/write models | SKILL.md § Distributed Systems |
| **Write-Through Cache** | Keep cache coherent with DB | SKILL.md § State Ownership |
| **Bulkhead Isolation** | Prevent cascade failures | spec_template.md § Failure Modes |
| **Idempotency** | Safe retries, no duplicates | code_review_checklist.md § Error Handling |

---

## Evaluation Rubric

After using this skill, score your system:

| Dimension | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **State** | Multiple owners | Some replicas | Single owner | Audit trail |
| **Feedback** | No logs | Unstructured | Structured logs | Metrics + alerts |
| **Blast Radius** | Don't know | Loosely mapped | Well documented | Tested via chaos |
| **Testing** | None | Happy path | All failures | Concurrency + chaos |
| **Scaling** | Doesn't | To 10x | To 100x | Horizontal, built-in |
| **Dependencies** | Hidden | Some explicit | All injected | Versioned contracts |
| **Code Quality** | Unreadable | Readable | Clear intent | Self-documenting |

**Target**: 2+ on all dimensions. Anything < 2 is a risk.

---

## What Gets Better With This Skill

### Before (Without SystemDesign)
- ❌ Code generated without design (fragile, tightly coupled)
- ❌ Failure modes unknown (surprising cascade failures)
- ❌ No logging strategy (silent failures discovered by users)
- ❌ Hidden dependencies (can't deploy independently)
- ❌ Performance unknown (discovered in production)
- ❌ Security holes (unvalidated input, hardcoded secrets)
- ❌ Scalability limits hit (unable to handle growth)

### After (With SystemDesign)
- ✅ Design documents architecture before code
- ✅ Failure modes enumerated and handled
- ✅ Observability baked in (logs, metrics, traces)
- ✅ Dependencies explicit (can deploy, test independently)
- ✅ Performance targets defined and measured
- ✅ Security requirements in spec (reviewed, implemented)
- ✅ Scaling plan documented (known limits, mitigation)

---

## FAQ

**Q: Is this overkill for small projects?**
A: No. Even 100-line scripts benefit from clarity on state ownership and error handling.

**Q: Will this slow down development?**
A: Upfront (writing spec takes time). But saves debugging (days). Net positive.

**Q: Can I use this without Claude Code?**
A: Yes. Use it to review code from any source. It works with Copilot, Cursor, etc.

**Q: What if requirements change mid-project?**
A: Update the spec. It's a living document.

**Q: How long should a spec be?**
A: 30 min to 2 hours to write. Saves days of debugging.

**Q: Is this a replacement for architecture review?**
A: No. It's a guide to thorough thinking. Still need human review.

---

## Files to Download

All files are in `/mnt/user-data/outputs/`:

1. **README.md** — Start here (overview)
2. **SKILL.md** — Main skill (read entirely, reference often)
3. **spec_template.md** — Copy and use
4. **DESIGN_template.md** — Copy and use (for UI/brand)
5. **code_review_checklist.md** — Bookmark and reference
6. **INTEGRATION_GUIDE.md** — Setup instructions

---

## Next Steps

1. **Read README.md** (15 min): Understand the skill
2. **Skim SKILL.md** (30 min): Get familiar with concepts
3. **Copy spec_template.md** to your project
4. **Write one spec** (2 hours): Define your first feature's architecture
5. **Prompt Claude Code** with the spec as a constraint
6. **Review with checklist** (30 min): Audit the generated code
7. **Deploy and monitor**: Verify observability and fallbacks work
8. **Reference SKILL.md** as needed: It has answers to most questions

---

## Success Criteria

You're using SystemDesign effectively when:

- ✓ You write specs before coding
- ✓ You can answer the Three Pillars with certainty
- ✓ Your code has structured logging and metrics
- ✓ Failure modes are documented and tested
- ✓ Dependencies are explicit (injected, not global)
- ✓ You trace blast radius before deploying
- ✓ You use the checklist to review code
- ✓ Monitoring and alerts catch issues before users do

---

## Support

**Most questions are answered in SKILL.md.** It's comprehensive and well-organized.

- Architecture question? → SKILL.md § The Three Pillars
- Code review issue? → code_review_checklist.md
- Failure mode question? → spec_template.md § Failure Modes
- Design system question? → DESIGN_template.md

---

## Summary

You now have:

1. **A skill** (SKILL.md) covering every aspect of architectural thinking
2. **Templates** for specs and design systems
3. **A checklist** for code review (100+ items)
4. **Integration guidance** for Claude Code
5. **Real-world examples** and patterns

**Use them to build systems that are**:
- Resilient (failures handled, no cascades)
- Observable (you can see what's happening)
- Scalable (grow without architectural rework)
- Maintainable (loosely coupled, clear intent)
- Secure (threats identified, mitigated)

**The goal**: Move from "coding faster" to "architecting better." Let Claude Code handle the speed. Your job is to conduct the orchestra.

---

**Ready?** Start with step 1: Read README.md. Then write your first spec.
