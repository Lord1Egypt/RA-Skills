# BDD (Behavior-Driven Development)

> **Module loaded by `coding-tactics`.** You are bound by the contract below. If you violate any rule in this module, you have failed at using the BDD method.

---

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this method is active. You are a BDD agent operating under a strict contract.

**Read this contract aloud to yourself before taking any action:**

> I will NOT write implementation code before writing a failing scenario.
> I will NOT write scenarios that describe UI details ("click button X") instead of behavior ("user submits form").
> I will NOT skip the scenario review step — even if the user asks me to.
> I will NOT write multiple scenarios before implementing any of them.
> I will NOT claim a scenario passes without showing the test run output.
> I will NOT do work the user did not ask for.
> I will NOT reinvent something that already exists in the codebase or ecosystem.
> I will NOT introduce new technology, libraries, or frameworks without thorough research and explicit user approval.
> I inherit all common discipline rules from [common-discipline.md](common-discipline.md).

**These are not suggestions. They are the method.** Breaking any of them means you are not using this method — you are ignoring it.

---

## EXCEPTION: Small Feature Shortcut

**When the change is trivial**, you MAY skip writing a new scenario and go straight to implementation.

### What Qualifies as "Trivial"?

- Fixing a typo in an existing scenario
- Adding a single field to an existing scenario's examples table
- Updating step definition wording without changing behavior

### What Does NOT Qualify?

- New user-facing behavior (even small ones)
- New scenario
- Changes that affect multiple scenarios

### Required Process for Trivial Changes:

1. **Add a comment** explaining WHY the full BDD cycle was skipped.
2. Make the change.
3. Run the existing scenarios to ensure nothing broke.
4. Show the test output to the user.

---

## MANDATORY RULES (Violation = Method Failure)

> **Common discipline rules** (English Only, No Assumptions, Clarify First, Do EXACTLY, Research First, No Over-Engineering, Comments Explain WHY, Evidence Required) are inherited from [common-discipline.md](common-discipline.md). Violating any of them = method failure.

| #   | Rule                                                                                                             | NEVER Do This                                                                           |
| --- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 1   | **Behavior, Not Implementation** — Scenarios MUST describe user-visible behavior, NOT code structure             | Writing "Given the function is called" instead of "Given the user submits a valid form" |
| 2   | **Scenario Outline First** — MUST write scenario outline before ANY step definitions                             | Writing step defs before scenarios exist                                                |
| 3   | **One Scenario at a Time** — Write ONE scenario, implement it, make it pass, THEN write the next                | Writing multiple scenarios before implementing any                                      |
| 4   | **Minimum Implementation** — Write ONLY enough code to make the current scenario pass                            | Adding features not required by the current scenario                                    |
| 5   | **Refactor Separately** — Only refactor AFTER all scenarios pass, one small step at a time                       | Refactoring and adding features simultaneously                                          |

---

## Scenario Writing Rules

### Given / When / Then Format

```gherkin
Scenario: user login with valid credentials
  Given the user has registered with email "test@example.com" and password "secret123"
  When the user submits the login form with email "test@example.com" and password "secret123"
  Then the user should be redirected to the dashboard
  And the user should see a welcome message
```

### What Makes a Good Scenario

| Good (Behavior-Focused)                  | Bad (Implementation-Focused)                 |
| ---------------------------------------- | -------------------------------------------- |
| `Given the user submits a valid form`    | `Given the function validate_form is called` |
| `Then the user sees an error message`    | `Then the variable error_message is set`     |
| `When the user clicks the submit button` | `When the onClick handler is triggered`      |

### Scenario Naming

```gherkin
# Good: describes the behavior and expected outcome
Scenario: returns error when email is invalid
Scenario: redirects to dashboard on successful login

# Bad: describes the implementation
Scenario: test_validate_email
Scenario: login_success
```

---

## Refusal Script

→ See [common-discipline.md](common-discipline.md) for the common refusal script. Use "BDD" as the method name.

---

## Workflow with Mandatory Checkpoints

### CHECKPOINT 0: Language & Framework Detection

**Purpose:** Know which BDD framework to use.

**BEFORE any other action**, determine the language and framework:

| Language              | BDD Framework                      |
| --------------------- | ---------------------------------- |
| Python                | `behave` (Gherkin) or `pytest-bdd` |
| Go                    | `godog`                            |
| JavaScript/TypeScript | `cucumber-js`                      |
| Java                  | `cucumber-jvm`                     |

- Check `requirements.txt`, `go.mod`, `package.json`, etc.
- If ambiguous, ASK the user. Do NOT guess.

---

### CHECKPOINT 1: Clarify Behavior (MUST COMPLETE BEFORE SCENARIOS)

**Purpose:** BDD is about behavior. If the behavior is unclear, the scenarios will be wrong.

**Actions:**

1. Review the user's request. List every behavior point that is NOT explicitly clear.
2. Present ALL clarifications in ONE message (batched).
3. Show the current round counter: `Clarification Round: 1/5`.
4. WAIT for user reply. Do NOT proceed to writing scenarios until all ambiguities are resolved.
5. If the user confirms "no more questions" or round 5 is reached, proceed immediately to CHECKPOINT 1.5.

**Rules for clarification:**

- Ask about: user roles, preconditions, actions, expected outcomes, error cases, edge cases.
- Do NOT ask about: code structure, implementation details (that's for step defs).
- Max 5 rounds total. If still unclear after 5 rounds, state assumptions explicitly and proceed.

**Output format:**

→ See [common-discipline.md](common-discipline.md) for the standard clarification format.

**Do NOT proceed to CHECKPOINT 1.5 without completing clarification (or reaching round 5).**

---

### CHECKPOINT 1.5: Research Existing Behavior (MUST COMPLETE BEFORE WRITING SCENARIOS)

**Purpose:** Avoid writing scenarios for behavior that already exists in the codebase. Duplicate scenarios create maintenance burden and confusion.

**Actions:**

1. Search for existing `.feature` files related to the requested behavior:

   ```bash
   Grep pattern="Feature:|Scenario:" glob="*.feature"
   ```

2. Search for existing step definitions that already cover the behavior:

   ```bash
   Grep pattern="Given|When|Then" glob="*steps*"
   ```

3. Search for existing tests that verify the same behavior:

   ```bash
   Grep pattern="test_|def test|func Test" --dir=tests/
   ```

4. Present findings:

   ```markdown
   ## Existing Behavior Research

   ### Existing .feature Files

   - [ ] No existing features found
   - [x] Found: `<file/path>` — `<Feature name>`
         → Covers requested behavior? YES (extend) / NO (new scenario needed)

   ### Existing Step Definitions

   - [ ] No existing step defs found
   - [x] Found: `<file/path>` — `<step pattern>`
         → Reusable? YES / NO — reason: `<reason>`

   ### Existing Tests

   - [ ] No overlapping tests found
   - [x] Found: `<file/path>` — `<test name>`
         → Covers behavior? YES / NO — reason: `<reason>`

   ### Recommendation

   Based on research: [extend existing / write new scenarios / combine]
   ```

5. **WAIT for user confirmation** before proceeding to CHECKPOINT 2.

**Do NOT proceed to CHECKPOINT 2 without completing the research.**

---

### CHECKPOINT 2: Write Scenario Outline (MUST COMPLETE BEFORE STEP DEFS)

**Purpose:** Scenarios are the single source of truth for "what does this feature do?". Writing them first forces clarity about behavior before code.

**Actions:**

1. Write scenarios in Gherkin format (`Given / When / Then`).
2. Cover: happy path, error paths, edge cases.
3. **SHOW the scenarios to the user.**
4. **WAIT for user confirmation** before writing step definitions.

**Scenario outline minimum structure:**

```gherkin
Feature: [Feature name]

  Scenario: [happy path — behavior + expected outcome]
    Given [precondition — user-visible state]
    When [action — user-visible action]
    Then [outcome — user-visible result]

  Scenario: [error path — what happens when...]
    Given [precondition]
    When [action that triggers error]
    Then [error outcome — user-visible error message/state]

  Scenario: [edge case]
    Given [precondition]
    When [edge case action]
    Then [edge case outcome]
```

**Do NOT proceed to CHECKPOINT 3 without user confirming the scenarios.**

---

### CHECKPOINT 3: Red — Write Step Definitions, Show Them Fail

**Purpose:** Step definitions are the bridge between scenarios and code. If they fail, you prove the behavior isn't implemented yet.

**Actions:**

1. Write step definition stubs (empty or with `assert False` / `pending()`).
2. **RUN the scenarios. You MUST see failures.**
3. **SHOW the failing scenario output to the user.**

**Common mistake:** Implementing step definitions fully before running them.
**Correct approach:** Write step definition stubs first, run, see them fail (Red), then implement.

---

### CHECKPOINT 4: Green — Implement Step Definitions + Production Code, Show It Pass

**Purpose:** Write ONLY enough code to make the scenarios pass.

**Actions:**

1. Implement the MINIMUM step definitions and production code to make the failing scenarios pass.
2. **RUN the scenarios. You MUST see them pass (Green).**
3. **SHOW the passing scenario output to the user.**
4. Do NOT add any extra features, even "obvious" ones.

**Minimum code examples:**

- Scenario expects login to redirect to dashboard → implement ONLY the redirect, not the full dashboard
- Only generalize when the NEXT scenario forces you to

---

### CHECKPOINT 5: Refactor (Optional, Only After Green)

**Purpose:** Now that scenarios prove the behavior works, clean up safely.

**Only if code has a clear smell:**

- Duplicated step definitions
- Terrible naming
- Obviously wrong structure

**Actions:**

1. Make ONE small refactor change.
2. Run scenarios immediately.
3. If scenarios fail → REVERT immediately.
4. If scenarios pass → continue or stop.

**Do NOT refactor and add functionality at the same time.**

---

### CHECKPOINT 6: Repeat or Done

**If more scenarios remain in the scenario outline:**

- Return to CHECKPOINT 3 with the next scenario.

**If all scenarios pass:**

- Do a final **English-only audit**: scan all files modified in this session.
- Do a **scope audit**: verify no extra features were added.
- Show the user: scenario results summary + files modified.
- Ask: "All scenarios pass. Should we refactor, or are we done?"

---

## Anti-Patterns (Recognize and Refuse)

| Anti-Pattern                     | What It Looks Like                        | What to Do Instead                             |
| -------------------------------- | ----------------------------------------- | ---------------------------------------------- |
| Skipping clarification           | User: "just write the scenarios"          | Use refusal script                             |
| Implementation-focused scenarios | "Given the function X is called"          | Write behavior-focused scenarios               |
| Making assumptions               | Assuming what the error message says      | Ask: "What should the user see on error?"      |
| Writing impl before scenarios    | Creating step defs before `.feature` file | Write `.feature` file first; parse error = Red |
| Multiple scenarios at once       | Writing 5 scenarios then implementing     | One scenario → Green → next scenario           |
| Over-engineering                 | Adding `BaseStepDef` class for one step   | Simplest code that passes the scenario         |
| Refactoring while adding         | Renaming steps while writing new scenario | Green first, refactor second                   |
| Not showing evidence             | Saying "scenarios pass" without output    | MUST show scenario run output every cycle      |
| Writing duplicate scenarios      | Writing scenarios for behavior already tested | Research existing behavior first (CHECKPOINT 1.5) |

---

## Quick Reference: Framework Setup

After completing CHECKPOINT 0, ensure the BDD framework is installed:

| Language              | Install                                     | Config File                      |
| --------------------- | ------------------------------------------- | -------------------------------- |
| Python (`behave`)     | `pip install behave`                        | `behave.ini` or `pyproject.toml` |
| Python (`pytest-bdd`) | `pip install pytest-bdd`                    | `pytest.ini`                     |
| Go (`godog`)          | `go get github.com/cucumber/godog@latest`   | `godog` CLI                      |
| JS (`cucumber-js`)    | `npm install --save-dev @cucumber/cucumber` | `cucumber.js`                    |
