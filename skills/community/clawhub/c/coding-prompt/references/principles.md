## 2. Core Principles

These are the foundational rules. They are not templates — they are lenses through which every coding prompt should be evaluated.

### 2.1 Use "Must NOT" Over "Should"

AI interprets prohibitions far more precisely than suggestions. "Should" creates a gradient; "must NOT" creates a cliff.

**Rule**: Replace every "应该/should" with a specific, quantifiable "不能/must NOT" when possible.

- Weak: `Code should be concise` → Strong: `Must NOT introduce new dependencies. Must NOT create utility classes used only once.`
- Weak: `Structure should be clear` → Strong: `Must NOT exceed 3 levels of nesting. Must NOT write functions over 50 lines.`
- Weak: `Algorithm should be smarter` → Strong: `Must NOT use hardcoded matching rules. Must use the LLM for judgment.`

**Quantification matters**: "Not too long" is still vague. "Under 50 lines per function" is actionable.

### 2.2 Scenario-First Design

The single most impactful pattern. AI designs from technical implementation by default (scan files → parse → store → index). But the best designs start from how the user actually uses the feature.

**Rule**: The first constraint in any feature prompt should be the usage scenario, not the technical requirement.

- Weak: `Implement a file snapshot system with save, restore, and diff support.`
- Strong: `My daily workflow: I edit a document, want to save a snapshot of it, and later see its change history and restore a previous version. Design based on this scenario.`

**Why**: AI has 100 implementation approaches in memory. Without a scenario anchor, it picks the "most general/powerful" one — which is usually over-engineered. With a scenario, it picks the "most fitting" one — which is usually simpler and better.

### 2.3 Give Constraints, Not Implementation Details

Define **what** it is and **where the boundaries are**. Let AI decide **how**.

**Rule**: Constraints should specify existence and boundaries, never prescribe specific function names, class hierarchies, or file structures — unless there's a proven reason.

- Good: `There must be a place to store all template metadata. The LLM reads the metadata and selects the appropriate template.`
  → AI chose `meta.json` — optimal solution, not prescribed.
- Bad: `Create a TemplateMetadataManager class with a get_matching_template() method.`

**Exception**: When integrating with existing code, naming/structure constraints are valid to maintain consistency.

### 2.4 Diagnose State Before Taking Action

Never assume the current state. Ask AI to check first, then act. This prevents modifying things that don't need modification, or breaking things that were already correct.

**Rule**: For any corrective action, lead with a diagnostic question.

- Weak: `Change the matching algorithm to LLM-driven.`
- Strong: `Check if the current matching algorithm is already LLM-driven. If yes, explain where. If no, modify according to these principles: ...`

**Impact**: Smaller change scope, fewer side effects, no unnecessary refactoring.

### 2.5 Question Requirements Before Implementing

AI defaults to additive thinking — the user must actively play the subtraction role.

**Rule**: For any non-trivial feature, answer three questions before implementation:
1. Why is this needed?
2. What's the simplest alternative?
3. What breaks if we remove it?

**Apply to both user's own ideas and AI's proposals.** A single "why do we need this?" eliminates more unnecessary complexity than any optimization pass.

### 2.6 Simplicity as Explicit Criterion

Given multiple technical options, AI will choose the most "powerful/flexible/general" one. Simplicity must be written into the evaluation criteria — it will never be the default.

**Rule**: When facing a technical decision, explicitly add simplicity as a criterion:
- Implementation complexity (LOC, dependency count)
- Debuggability (can problems be located quickly?)
- Comprehensibility (can a new team member understand it?)
- Unnecessary abstraction (are we over-engineering?)

**Default**: Pick the simplest option unless there's a concrete technical reason not to.

### 2.7 Verify Before Trusting

AI's "done" declaration is reliable ~60% of the time — "code written" ≠ "works correctly" ≠ "meets requirements".

**Rule**:
- **Pre-task**: Define acceptance criteria before starting, not after.
- **Post-task**: When AI says "complete", ask for verifiable evidence — actual output, file/function location, or a test run.
- **Never accept** "I've implemented X" without proof.

**For fake completion detection (D12)**, see `references/checklist.md`.

### 2.8 LLM-Native Over Rule-Based

Due to heavy exposure to traditional algorithm code in training data, AI has a systematic bias toward rule-based/hardcoded approaches — even when the LLM's own capabilities would produce a better, simpler, more robust solution.

**Common manifestations**:
- Template matching via hardcoded keyword lists instead of LLM semantic understanding
- Classification via if-else chains or regex instead of LLM judgment
- Content analysis via string operations instead of LLM comprehension
- Decision logic via lookup tables instead of LLM reasoning

**Rule**: When a feature involves understanding, matching, classifying, or decision-making about content (text, code, natural language), explicitly evaluate: **Can the LLM do this directly?** If yes, mandate LLM-native implementation.

- Weak: `Improve the template matching accuracy.`
- Strong: `Template matching must be done by the LLM reading template metadata and deciding which template to use. Must NOT use hardcoded keyword matching, regex, or scoring rules. The LLM's understanding is sufficient — do not add additional algorithm models.`

**Exception**: Rule-based approaches are appropriate for deterministic operations (file I/O, data format conversion, config parsing) where LLM judgment adds no value.
