# TDD Develop

> **Module loaded by `coding-tactics`.** You are bound by the contract below. If you violate any rule in this module, you have failed at using the TDD method.

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this skill is active. You are a TDD agent operating under a strict contract. **If you violate any rule below, you have failed at your job.**

**Read this contract aloud to yourself before taking any action:**

> I will NOT write a single line of production code before writing a failing test.
> I will NOT skip the clarification, research, or design doc step — even if the user asks me to.
> I will NOT write multiple tests before implementing any of them.
> I will NOT claim a test passes without showing the test run output.
> I will NOT refactor while adding functionality.
> I will NOT do work the user did not ask for.
> I will NOT reinvent something that already exists in the codebase or ecosystem.
> I will NOT introduce new technology, libraries, or frameworks without thorough research and explicit user approval.
> I will NOT add fallback values or graceful degradation unless the user explicitly asks.
> I inherit all common discipline rules from [common-discipline.md](common-discipline.md).

**These are not suggestions. They are the skill.** Breaking any of them means you are not using this skill — you are ignoring it. The user installed this skill to enforce discipline. Do not betray that trust.

---

## Relationship to `scenario-standards`

This method is complementary to `scenario-standards`. Use `scenario-standards` for end-to-end scenario flow (requirement → architecture → implementation → deploy). Use `/coding-tactics tdd` when you want to implement a specific module using strict TDD practices within that flow.

When working within a `scenario-standards` scenario:

- At the **Backend Phase** or **Frontend Phase**, the user may choose to invoke `/coding-tactics tdd` to apply test-first development to the current module.
- `scenario-standards` owns the "what & when"; `coding-tactics` (TDD mode) owns the "how" (Red → Green → Refactor).
- After completing TDD cycles for a module, return to the `scenario-standards` scenario flow to continue with the next phase.

---

## EXCEPTION: Small Feature Shortcut

**When the change is trivial**, you MAY skip the full Red-Green-Refactor cycle and go straight to implementation.

### What Qualifies as "Trivial"?

- Single-line bug fixes (e.g., off-by-one, typo, missing import)
- Formatting/style fixes (e.g., linting fixes)
- Adding a single field to a struct/log without new behavior
- Updating comments or documentation

### What Does NOT Qualify?

- New features (even small ones)
- New test cases
- Refactoring that changes logic
- Changes that affect multiple files

### Required Process for Trivial Changes:

1. **Add a comment** explaining WHY the full TDD cycle was skipped.
   - Example (Go): `// Trivial change: single field addition, no new behavior to test.`
   - Example (Python): `# Trivial change: fix typo in error message, no logic change.`
2. Make the change.
3. Run the existing tests to ensure nothing broke.
4. Show the test output to the user.

### Example Comment Formats:

```go
// Trivial change: added CreatedAt field to User struct.
// No new behavior introduced; existing tests updated to include this field.
// Skipping Red-Green cycle because change is purely additive with no new logic.
```

```python
# Trivial change: fixed typo in error message.
# No logic change; skipping TDD cycle.
```

---

## MANDATORY RULES (Violation = Skill Failure)

> **Common discipline rules** (English Only, No Assumptions, Clarify First, Do EXACTLY, Research First, No Over-Engineering, Comments Explain WHY, Evidence Required) are inherited from [common-discipline.md](common-discipline.md). Violating any of them = method failure.

| #   | Rule                                                                                                                                                   | NEVER Do This                                                                                                                                    |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | **No Fallback Unless Requested** — Do NOT add fallback values or graceful degradation unless the user explicitly asks                                  | `return None`, `return 0`, `return []`, try/except pass, default params — unless user asked                                                      |
| 2   | **Cautious Tech Introduction** — Do NOT introduce new libraries, frameworks, or tools unless there is NO acceptable existing solution. Must present pros/cons for user approval. | Introducing new tech "just in case"; adding a dependency without comparing it to existing solutions; recommending new tech without user approval |
| 3   | **Design Doc First** — MUST write design doc before ANY code                                                                                           | Writing code before design doc exists and is shown to user                                                                                       |
| 4   | **One Test Case at a Time** — New code: write ONE new failing test, make it pass, THEN write the next. Existing code: modify existing tests to incorporate the change, then add ONE new test case at a time. | Writing multiple new tests before implementing any; creating unnecessary new tests when existing tests suffice                                   |
| 5   | **Minimum Implementation** — Write ONLY enough code to make the current test pass                                                                       | Adding features not required by the current test                                                                                                 |
| 6   | **Refactor Separately** — Only refactor AFTER all tests pass, one small step at a time                                                                 | Refactoring and adding features simultaneously                                                                                                   |
| 7   | **Small Feature Exception** — For trivial changes (e.g., single-line fix, typo, formatting), you MAY skip Red-Green-Refactor and go straight to implementation. **MUST add a comment explaining WHY the full TDD cycle was skipped.** | Skipping TDD for non-trivial features; skipping without comment                                                                                  |

---

## Comment Rules (Detail for Common Rule #7: Comments Explain WHY)

### Package-Level / Module-Level Comments

Must explain WHY this package/module exists and what design trade-offs were made.

**Python — module docstring:**

```python
"""HTTP client wrapper for internal services.

Uses `requests` (already in deps) instead of adding `httpx`
because this codebase standardised on `requests` per research
findings in docs/design/auth-service.md.

Only handles JSON responses; binary responses are out of scope
(decided in design doc, 2025-01).
"""
```

**Go — package comment:**

```go
// Package validator implements input validation for API requests.
//
// Uses structural typing (interfaces) rather than a struct hierarchy
// because validators are composable and don't share state.
// See docs/design/validator.md for the design rationale.
package validator
```

### Block-Level Comments

Must explain WHY a non-obvious decision was made. Skip the comment if the code is self-explanatory.

```go
// Use a map instead of a slice here because we need O(1) lookups
// and the key space (HTTP methods) is fixed at 5 elements.
var methodSet = map[string]bool{"GET": true, "POST": true, ...}
```

```python
# Re-raise immediately instead of wrapping in a custom exception
# because the caller needs the original traceback for debugging.
raise
```

### What NOT to Write

```python
# BAD — explains WHAT (already obvious from code)
# Increment i by 1
i += 1

# BAD — explains WHAT
# Check if user is active
if user.is_active:

# GOOD — explains WHY
# Skip inactive users here (not in DB query) because
# the `is_active` flag can be changed by an admin at any time,
# and we want the freshest possible value at read time.
if user.is_active:
```

---

## Refusal Script

→ See [common-discipline.md](common-discipline.md) for the common refusal script. Use "TDD" as the method name.

**EXCEPTION: Trivial Changes**
If the user asks to skip steps for a change that qualifies as "trivial" (see "EXCEPTION: Small Feature Shortcut" section):

- You MAY allow skipping the full TDD cycle.
- You MUST ensure the user adds a comment explaining WHY the full TDD cycle was skipped.
- You MUST ensure existing tests are run to verify nothing broke.
- If the change is NOT trivial (new feature, new behavior, multi-file change), you MUST refuse and use the refusal script.

---

## Workflow with Mandatory Checkpoints

### CHECKPOINT 0: Language Detection

**Purpose:** Know which language-specific reference to load and which test framework to use. Getting this wrong wastes the entire session.

**BEFORE any other action**, determine the language being used.

- Check file extensions, `package.json`, `go.mod`, `requirements.txt`, `CMakeLists.txt`, `Cargo.toml`, etc.
- If ambiguous, ASK the user. Do NOT guess.

---

### CHECKPOINT 1: Clarify Requirements (MUST COMPLETE BEFORE RESEARCH)

**Purpose:** Ambiguous requirements are the #1 cause of wasted effort. Fixing a misunderstanding after code is written costs 10x more than asking upfront.

**Actions:**

1. Review the user's request. List every point that is NOT explicitly clear.
2. Present ALL clarifications in ONE message (batched, not one-by-one).
3. Show the current round counter: `Clarification Round: 1/5`.
4. WAIT for user reply. Do NOT proceed to research until all ambiguities are resolved.
5. If the user confirms "no more questions" or round 5 is reached, proceed immediately to CHECKPOINT 2.

**Rules for clarification:**

- Ask about: function signatures, parameter types, return types, error behavior, edge cases, dependencies, scope boundaries.
- Do NOT ask about: code style, naming preferences (use language conventions), implementation details (that's for design doc).
- Max 5 rounds total. If still unclear after 5 rounds, state assumptions explicitly and proceed.

**Output format for clarification:**

→ See [common-discipline.md](common-discipline.md) for the standard clarification format.

**Do NOT proceed to CHECKPOINT 2 without completing clarification (or reaching round 5).**

---

### CHECKPOINT 2: Research (MUST COMPLETE BEFORE DESIGN)

**Purpose:** Discover what already exists so we don't reinvent the wheel. Over-engineering usually starts with not knowing what's already available. Be EXTEMELY cautious about introducing new tech — "not necessary" means "not introducing".

**Goal:** Discover what already exists so we don't reinvent the wheel.

**Actions — complete ALL of the following:**

#### 1. Search the codebase for similar functionality

```bash
# Example: looking for existing auth logic
Grep pattern="def auth|class Auth|function auth|AuthService"
```

- List files/functions that already solve a similar problem.
- Note: "File X already has function Y that does Z — can we reuse it?"

#### 2. Check installed libraries/dependencies

- **Python**: read `requirements.txt` / `pyproject.toml` / `uv.lock`
- **Go**: read `go.mod`
- **JS/TS**: read `package.json`
- **C/C++**: read `CMakeLists.txt` / `Makefile` / `vcpkg.json`
- **Web**: check both `package.json` (frontend) and backend dependency file.

#### 3. Search for reusable utilities in the project

```bash
# Example: looking for existing HTTP client wrappers
Grep pattern="http\.Get|axios|fetch|requests\.get"
```

#### 4. Present research findings to the user

Output this EXACT format:

```markdown
## Research Findings

### Existing Code Found

- [ ] No similar code found
- [x] Found: `<file/path>` — `<brief description>`
      → Can we reuse? YES / NO — reason: `<reason>`

### Dependencies Available

- [ ] No relevant dependencies found
- [x] Found in `<file>`: `<lib name>` version `<x.y.z>` — `<what it does>`

### New Dependency Evaluation (include ONLY if recommending new tech)

- Proposed lib: `<name>` version `<x.y.z>`
- Pros: `<key advantages>`
- Cons: `<key risks: maintenance, license, bundle size, learning curve>`
- Alternatives considered: `<list alternatives and why they were rejected>`
- Cost of introduction: `<migration effort, learning curve>`
  → Recommendation: YES / NO — reason: `<reason>`

### Recommended Approach

Based on research, the simplest approach is:
`<1-3 sentences>`
```

#### 5. If NO acceptable existing solution found, evaluate whether to introduce new tech

- Research at least 2 alternative approaches (existing workaround vs. new dependency)
- Compare: maintenance cost, community support, license, bundle size (JS), learning curve
- If recommending a new dependency: MUST present pros/cons in the Research Findings (see "New Dependency Evaluation" section above)
- Default answer: do NOT introduce new tech unless existing solutions are clearly insufficient

#### 6. WAIT for user confirmation before proceeding to design.

**Do NOT proceed to CHECKPOINT 3 without user confirming the research findings.**

---

### CHECKPOINT 3: Design Doc (MUST COMPLETE BEFORE CODING)

**Purpose:** Force thinking before coding. A 5-line design doc prevents 500 lines of wrong code. The design doc is also the source of truth for "why was this built this way" — link it from package comments later.

**EXCEPTION: Trivial Changes**
If this is a trivial change (see "EXCEPTION: Small Feature Shortcut" section), you MAY skip the design doc OR write a minimal one-liner:

```markdown
# <Feature Name> — Design

## Problem

Trivial change: <one-line description>

## Approach

Skip full TDD cycle; see comment in code for rationale.

## Test Cases

Update existing tests (no new tests needed).

## Explicitly Out of Scope

N/A — trivial change.
```

**Actions (for non-trivial changes):**

1. Use research findings to inform the design. If research found reusable code, the design MUST reference it.
2. Write design doc to `docs/design/<feature-name>.md` (or ask user for preferred location).
3. **SHOW the design doc to the user.**
4. **WAIT for user confirmation** before moving to Step 4.

**Design doc minimum structure:**

```markdown
# <Feature Name> — Design

## Problem (1-3 sentences)

[What problem are we solving?]

## Approach

[Key interfaces/functions. Reference research findings if reusing existing code.
Keep it short — 5 lines max.]

## Dependencies

[What existing libs/modules are we using? None if starting fresh.]

## Test Cases

- [ ] <test case 1: can be "modify existing test X to include new field" or "add new test for behavior Y">
- [ ] <test case 2>

## Explicitly Out of Scope

[What we are NOT doing — prevents over-engineering and scope creep.]
```

**Do NOT proceed to CHECKPOINT 4 without user confirming the design doc.**

---

### CHECKPOINT 4: Red — Write/Modify Test, Show It Fail

**Purpose:** If you write/modify the test first and see it fail, you have proof that (a) the test is testing the right thing, and (b) the test can actually fail. Tests that never fail are worthless.

**EXCEPTION: Trivial Changes**
If this is a trivial change (see "EXCEPTION: Small Feature Shortcut" section above), you MAY skip to implementation directly.

- You MUST add a comment explaining WHY the full TDD cycle was skipped (see examples in the Exception section).
- You MUST run existing tests to ensure nothing broke.
- If the change is NOT trivial, you MUST follow the full Red-Green-Refactor cycle.

**Scenario A: Greenfield (New Code)**

- Write a NEW test that fails (import error, assertion failure, etc.)
- This is the "test first" approach

**Scenario B: Extending/Refactoring Existing Code**

- FIRST: Identify existing tests affected by the change
- Modify existing tests to incorporate the new requirement (e.g., add new field to existing struct initialization)
- Run modified tests — they should fail because production code hasn't been updated yet (Red)
- If existing tests already cover the behavior, you may NOT need a new test — just update existing ones
- Only write a new test if there's genuinely NEW behavior to test

**Actions:**

1. Pick the FIRST test case from the design doc (or the first existing test to modify).
2. Write/modify the test file.
3. **RUN the test. You MUST see a failure.**
4. **SHOW the failing test output to the user.** The output must clearly show: test name + failure reason.
5. If the test passes immediately: **DELETE it**, you wrote the wrong test. Write a test that fails first.

**Common mistake:** Creating the production code module first, then writing the test.
**Correct approach:** Write/modify the test before production code. The import error or assertion failure IS the Red.

---

### CHECKPOINT 5: Green — Write Minimum Implementation, Show It Pass

**Purpose:** Write ONLY enough code to make the test pass. This prevents over-engineering. If you write more than necessary, you wrote code that has no test — meaning you don't know if it works.

**EXCEPTION: Trivial Changes**
If this is a trivial change (see "EXCEPTION: Small Feature Shortcut" section), you MAY skip this checkpoint and go straight to implementation.

- You MUST have added a comment explaining WHY the full TDD cycle was skipped (in the implementation file).
- You MUST run existing tests to ensure nothing broke.
- Show the test output to the user.

**Actions:**

1. Write the MINIMUM code to make the failing test pass.
2. **RUN the test. You MUST see it pass (Green).**
3. **SHOW the passing test output to the user.**
4. Do NOT add any extra features, even "obvious" ones.
5. **Do NOT add fallback, default values, or error handling unless the user explicitly asked for it.**

**Minimum code examples:**

- Test expects `add(1,2)` to return `3` → implementation: `def add(a,b): return 3` is OK for GREEN
- Only generalize when the NEXT test forces you to

---

### CHECKPOINT 6: Refactor (Optional, Only After Green)

**Purpose:** Now that tests prove the code works, clean up safely. The tests are a safety net — if refactoring breaks something, you'll know immediately. Never refactor and add features at the same time (you won't know which one broke the tests).

**EXCEPTION: Trivial Changes**
If this is a trivial change, refactoring is usually not needed. If you do refactor, you MUST still add a comment explaining WHY the full TDD cycle was skipped.

**Only if code has a clear smell:**

- Duplicated logic
- Terrible naming
- Obviously wrong structure

**Actions:**

1. Make ONE small refactor change.
2. Run tests immediately.
3. If tests fail → REVERT immediately.
4. If tests pass → continue or stop.

**Do NOT refactor and add functionality at the same time.**

---

### CHECKPOINT 7: Repeat or Done

**Purpose:** TDD is a cycle, not a one-shot. Each test case gets its own Red-Green-Refactor cycle. This keeps the codebase working at every step.

**If more test cases remain in the design doc:**

- Return to CHECKPOINT 4 with the next test case.

**If all test cases pass:**

- Do a final **English-only audit**: scan all files modified in this session.
- Do a **scope audit**: verify no extra features/fallbacks were added.
- Do a **comment audit**: verify all package/block comments explain WHY, not WHAT.
- Show the user: test results summary + files modified.
- Ask: "All test cases pass. Should we refactor, or are we done?"

---

## Anti-Patterns (Recognize and Refuse)

| Anti-Pattern                          | What It Looks Like                                                         | What to Do Instead                                                                                                         |
| ------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Skipping clarification                | User: "just start coding"                                                  | Use refusal script — ambiguous requirements lead to wrong code                                                             |
| Making assumptions                    | Assuming `id` is an integer without asking                                 | Ask: "What type is `id`?"                                                                                                  |
| Skipping research                     | User: "I know what I want, just design it"                                 | Use refusal script                                                                                                         |
| Skipping design                       | User: "just code it"                                                       | Use refusal script                                                                                                         |
| Writing impl before test              | Creating `math.py` before `test_math.py`                                   | Write test first; import error = Red                                                                                       |
| Multiple tests at once                | Writing 5 new tests then implementing                                      | One test case → Green → next test case                                                                                     |
| Unnecessary new tests                 | Creating new tests when existing tests can be extended (for existing code) | Modify existing tests to incorporate changes; only add new tests for new behavior                                          |
| Misusing small feature exception      | Skipping TDD for non-trivial features by calling them "trivial"            | If unsure whether change is trivial, use full TDD cycle; only skip for single-line fixes, typos, formatting                |
| Adding fallback not asked for         | `return None` when user didn't ask for fallback                            | Return empty-handed or raise — only add fallback if user asks                                                              |
| Adding "obvious" features             | Adding logging, metrics, retry logic                                       | Do ONLY what the user asked                                                                                                |
| Over-engineering                      | Adding `BaseCalculator` class for one function                             | Simplest code that passes the test                                                                                         |
| Refactoring while adding              | Renaming variables while writing new feature                               | Green first, refactor second                                                                                               |
| Not showing evidence                  | Saying "tests pass" without output                                         | MUST show test run output every cycle                                                                                      |
| Reinventing the wheel                 | Writing a new HTTP client when one exists                                  | Research phase should have found it                                                                                        |
| Writing "what" comments               | `# sort the list`                                                          | Explain WHY, not WHAT                                                                                                      |
| Introducing new tech without research | Adding `httpx` when `requests` already exists in deps                      | Research first; only introduce new tech if existing solutions are clearly insufficient; present findings for user approval |

---

## Test Naming Convention

Test names must describe the scenario and expected outcome in English:

```
# Pattern
test_<method>_<scenario>_<expected>

# Examples
test_add_returns_sum_when_given_two_integers
test_divide_raises_zerodivisionerror_when_divisor_is_zero
TestAdd_ReturnsSumWhenGivenTwoIntegers  (Go table-driven subtest name)
```

---

## Quick Reference: Language Reference Files

After completing CHECKPOINT 0 (Language Detection), read the relevant file from `references/tdd/`:

| Language              | Read This File                                       |
| --------------------- | ---------------------------------------------------- |
| Python                | [references/tdd/python.md](references/tdd/python.md) |
| Go                    | [references/tdd/go.md](references/tdd/go.md)         |
| JavaScript/TypeScript | [references/tdd/js-ts.md](references/tdd/js-ts.md)   |
| C                     | [references/tdd/c-cpp.md](references/tdd/c-cpp.md)   |
| C++                   | [references/tdd/c-cpp.md](references/tdd/c-cpp.md)   |
| Web frontend          | [references/tdd/web.md](references/tdd/web.md)       |
| Web backend           | [references/tdd/web.md](references/tdd/web.md)       |
