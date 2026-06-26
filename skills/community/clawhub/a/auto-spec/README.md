<img width="1738" height="905" alt="Auto-Spec" src="https://github.com/user-attachments/assets/f16b0339-feea-4d38-8ac0-a52774948429" />

# Auto Spec

An Agent skill for **Spec-Driven Development** with disposable specs.

Write specs before coding, or extract them from existing code when needed.

## 🎯 When to Use

Trigger this skill when you want to:
- **Design before coding**: *"I want to add feature X, help me think it through first"* or *"Write me a spec for..."*
- **Understand existing code**: *"What does this code actually do, walk me through it"* or *"Reverse-engineer a spec from this module"*
- **Align on intent**: Ensure you and the AI are on the same page before it generates complex logic.

## 💡 Philosophy

> **Code is the single source of truth.**

Specs are **inputs** — they help humans align intent and assist AI coding — not deliverables. Specs don't need to stay in sync with code permanently; regenerate from code when needed.

Three hard constraints follow:
1. **No bidirectional binding, no CI drift detection** — that's life support for dead docs, expensive and fragile.
2. **Specs are disposable** — once landed, mission complete; code and tests take over as truth.
3. **To see current state, reverse-engineer from code** — don't maintain a static doc that can't keep up.

*Note: By default, Auto Spec presents specs directly in the conversation rather than writing them to files, treating them as temporary conversational snapshots.*

## 🆚 Auto Spec vs. Spec-kit / OpenSpec

While traditional spec tools like **Spec-kit** or **OpenSpec** treat specs as formal, long-lived documentation, **Auto Spec** takes a fundamentally different, lightweight approach optimized for AI-assisted coding:

| Feature | Auto Spec | Spec-kit / OpenSpec |
| :--- | :--- | :--- |
| **Source of Truth** | **Code only.** The spec is just an input for alignment. | Treats the spec as a parallel or primary source of truth. |
| **Lifecycle** | **Disposable.** Read, align, code, then discard. | **Persistent.** Maintained alongside the codebase. |
| **Sync Mechanism** | **None.** Regenerate from code dynamically when needed. | **Bidirectional binding** or strict CI drift detection. |
| **Format & Output** | **Conversational.** Focused on human-AI alignment (Markdown). | **Strict schemas** (JSON/YAML/XML) or formal documentation. |
| **Maintenance Cost**| **Zero.** No "dead docs" to maintain. | **High.** Requires constant updates to prevent drift. |

## 🔄 Two Modes

### Mode A: Forward Spec (Spec before code)

User has an idea but no code yet. Turn vague intent into precise behavioral contracts, then (optionally) implement according to the spec.
- Understands intent and asks targeted questions for edge cases.
- Generates a structured spec based on existing code context.
- Iterates with you until alignment is reached, then implements the code if requested.

### Mode B: Reverse Spec (Spec from code)

Code already exists. Extract behavioral contracts from code to understand what it actually does, or to establish a baseline before modifications.
- Extracts factual behavior, not guessed intent.
- Flags suspicious patterns, potential bugs, or legacy logic.
- Serves as a pre-change baseline for safe refactoring.

## 📝 Spec Format & Granularity

Auto Spec automatically adjusts the granularity of the spec based on your scope (Function, Module, Feature, or System level). 

A generated spec focuses on **Behavioral Contracts**, typically including:
- **Scenarios**: Preconditions, Inputs, Expected behavior, Postconditions, and Error cases.
- **Constraints & Boundaries**: Performance, security, business rules, and what the system *doesn't* do.
- **Dependencies**: External systems, interfaces, and dependents.

**Key Writing Principles:**
- **Precision over completeness**: One clear contract beats ten vague descriptions.
- **Behavior, not implementation**: Describes *what*, not *how*.
- **Uncertainty marking**: Uses `[TBD]` or `[NOTE]` tags instead of false confidence.

## 📊 Eval Results

Evaluated against 3 test cases covering both modes and multiple granularity levels:

| Test Case | With Skill | Baseline | Delta |
|---|---|---|---|
| Forward Spec (feature-level) | **7/7 (100%)** | 4/7 (57%) | +43% |
| Reverse Spec (module-level) | **7/7 (100%)** | 5/7 (71%) | +29% |
| Forward Spec + Code (function-level) | **7/7 (100%)** | 6/7 (86%) | +14% |
| **Total** | **21/21 (100%)** | **15/21 (71%)** | **+29%** |

Key improvements with the skill:
- **Structured behavioral scenarios** (preconditions/inputs/expected behavior/postconditions/exceptions)
- **Uncertainty marking** with `[TBD]` / `[NOTE]` tags instead of false confidence
- **Behavior-oriented** (what, not how) — avoids leaking implementation details into specs
- **Insight discovery** in reverse specs — flags suspicious code patterns

Full eval outputs are in the `evals/` directory.

## 📄 License

MIT
