# DoubleAgent Architecture Reference

## Theoretical Foundation

### Why AI Self-Evaluation Fails

AI self-evaluation bias is a structural problem, not a capability problem. Even the most powerful models fail when evaluating their own output because:

1. **Anchoring bias**: The generator has already committed to its approach. Evaluation happens in the context of "how can I justify this?" rather than "does this actually work?"
2. **Knowledge-assumption gap**: The generator knows what it *intended* — so it mentally fills in gaps that a real user would encounter as bugs
3. **Optimization misalignment**: The generator optimizes for "plausible completion" while quality requires "actual correctness"

The fix is architectural, not prompting-based. Separating roles at the agent level eliminates these biases structurally.

### GAN Analogy

The Generator-Evaluator architecture mirrors the **Generative Adversarial Network (GAN)** dynamic:
- **Generator** → Tries to produce output that passes the Evaluator
- **Evaluator** → Tries to identify failures the Generator would overlook
- **Tension** → Drives quality upward through adversarial pressure

Unlike GANs, the AI DoubleAgent loop uses natural language feedback instead of gradient descent — making it inspectable and steerable.

---

## Architecture Variants

### Variant A: Sequential (Default)
Best for: UI/code generation, content creation

```
Spec → Generator → Artifact → Evaluator → Score/Feedback → Generator (loop)
```

- Simple, reliable, easy to implement
- Each round: Generator reads full history, Evaluator reads only spec + artifact
- Loop control: exit on score ≥ threshold OR max rounds reached

### Variant B: Parallel Sampling + Selection
Best for: Exploring multiple solutions quickly

```
Spec → Generator × N (parallel) → N artifacts → Evaluator → Best selection
```

- Run 3-5 generator variants simultaneously
- Evaluator scores all, picks the best one to continue with
- Reduces risk of generator getting stuck in a local minimum

### Variant C: Staged Pipeline
Best for: Complex systems with multiple quality dimensions

```
Spec → Generator → Artifact
                      ↓
              Functional Evaluator (does it work?)
                      ↓ pass
              UX Evaluator (is it usable?)
                      ↓ pass
              Design Evaluator (is it beautiful?)
```

- Each evaluator is specialized for one dimension
- Failure at any stage sends feedback back to Generator with specific context
- Efficient: stops early if fundamentals are broken

### Variant D: Human-in-the-Loop
Best for: High-stakes outputs (production features, user-facing copy)

```
... (automatic loop) ... → Score ≥ 70 → Human Review → Approve/Adjust → Final
```

- Automatic rounds handle obvious issues
- Human review only when automatic evaluation says "probably good"
- Reduces human cognitive load by 80%+ while maintaining oversight

---

## Spec Contract Template

A well-formed spec enables both agents to work independently. Use this template:

```markdown
# Spec: [Feature/Task Name]
Version: 1.0
Date: YYYY-MM-DD

## Goal
[One sentence: what should exist when this is done?]

## Functional Requirements
- FR-001: [Specific, testable requirement]
- FR-002: [...]

## Interaction Specifications
- UI-001: [User clicks X → Y happens]
- UI-002: [Form field Z accepts input type W]

## Acceptance Criteria
- AC-001: [Measurable outcome that proves FR-001 works]
- AC-002: [...]

## Out of Scope
- [Things explicitly NOT required for this iteration]

## Test Scenarios
Scenario 1: [Happy path — normal user flow]
Scenario 2: [Edge case — empty data, error state]
Scenario 3: [Boundary — max input, concurrent action]
```

---

## History Format

The iteration history passed to the Generator should follow this structure:

```json
{
  "rounds": [
    {
      "round": 1,
      "score": 42,
      "score_breakdown": {
        "functional_completeness": 8,
        "interaction_quality": 12,
        "edge_cases": 6,
        "code_quality": 10,
        "craft": 6
      },
      "failures": [
        {
          "requirement": "FR-003",
          "observation": "Clicking submit button produces no response when form is empty",
          "severity": "high",
          "screenshot": "round1_failure_submit.png"
        }
      ],
      "passes": ["FR-001", "FR-002"],
      "evaluator_note": "Core navigation works but form validation is completely missing"
    }
  ],
  "trend": "improving",
  "recommendation": "continue"
}
```

**Trend values**: `improving` | `plateauing` | `degrading`
**Recommendation values**: `continue` | `switch_approach` | `accept` | `escalate`

---

## Loop Control Logic

```
Round N complete → Evaluate score

IF score >= PASS_THRESHOLD:
    → Accept output, exit loop

IF round >= MAX_ROUNDS:
    → Exit with best-scoring output, flag for human review

IF trend == "plateauing" AND round >= 3:
    → Signal Generator to switch approach (new design, new strategy)
    → Reset approach_switch_count

IF approach_switch_count >= 3:
    → Escalate to human: loop is stuck
```

**Recommended thresholds**:
| Use Case | PASS_THRESHOLD | MAX_ROUNDS |
|----------|---------------|------------|
| Internal tool / prototype | 70 | 10 |
| User-facing feature | 85 | 15 |
| Production critical | 95 | 20 + human review |

---

## Evaluator Independence Principles

To maintain evaluator independence across rounds:

1. **Fresh context per round**: Do not pass the Generator's reasoning to the Evaluator
2. **Spec anchoring**: Evaluator's system prompt starts with the original spec, not the artifact
3. **No self-reference**: Evaluator should not read the Generator's commit messages or inline comments
4. **Action-first evaluation**: Evaluator must *use* the artifact before reading code (prevents reasoning from artifact internals rather than user experience)
5. **Structured output only**: Evaluator outputs structured JSON, never free-form "it looks good" — prevents sycophantic drift

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Same agent self-evaluates | Cognitive anchoring bias | Separate agents with separate prompts |
| Evaluator reads Generator's comments | Grades intent, not reality | Show Evaluator only the deployed artifact |
| Vague scoring ("7/10 looks fine") | Unactionable feedback | Require score breakdown per rubric dimension |
| No calibration examples | Score inflation/drift | Run on 3-5 known examples first |
| Skip real interaction, read code only | Misses UI bugs, UX failures | Playwright for UI; always run, never skip |
| Max rounds = 3 | Generator never converges | Use 10-15 rounds minimum for complex outputs |
| Never reset approach | Gets stuck in local minimum | Switch strategy after 3+ plateauing rounds |

---

## DeepFMT Application Guide

For the DeepFMT system (Taro + React multi-platform), apply DoubleAgent as follows:

### Generator Agent = `coder` subagent
- Input: Sprint spec + previous evaluation history
- Task: Implement component/feature in Taro React TypeScript
- Output: Committed code + deployed preview URL

### Evaluator Agent = `tester` subagent (upgraded)
- Input: Sprint spec + preview URL (NOT coder's code)
- Task: Operate the H5/WeChat mini-program preview as a real patient/doctor user
- Tool: Playwright MCP → click buttons, fill diagnosis forms, navigate flows
- Output: Structured JSON score + screenshot evidence + failure list

### Key User Flows to Evaluate (per Sprint)
1. Patient onboarding flow: Register → Initial assessment → FMT recommendation
2. Doctor workflow: Patient list → Case review → Treatment record
3. Report generation: Input data → PDF report → Share link
4. Multi-platform consistency: H5 vs WeChat mini-program visual/functional parity

### Pass Threshold by Phase
- Phase 0 (framework migration): 75 — basic navigation and rendering
- Phase 1 (core features): 85 — all primary flows working
- Phase 2 (polish): 92 — edge cases and UX quality
