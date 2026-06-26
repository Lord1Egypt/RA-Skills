---
name: superpowers
description: >
  Agentic software development methodology — 13 integrated skills for
  disciplined AI-assisted development covering brainstorming, planning,
  TDD, debugging, code review, git worktrees, and branch management.
metadata:
  openclaw:
    emoji: "⚡"
---

# Superpowers

Disciplined, systematic approach to AI-assisted software development. 13 integrated skills covering the full development lifecycle.

## The 7-Step Workflow

1. **Brainstorm** — Design before implementation (Section 2)
2. **Plan** — Write detailed implementation plan (Section 3)
3. **Execute** — Implement with subagents or batches (Sections 4-6)
4. **Test** — TDD throughout: RED-GREEN-REFACTOR (Section 7)
5. **Debug** — Systematic root cause analysis when needed (Section 8)
6. **Review** — Code review after each task (Section 10)
7. **Finish** — Branch completion and integration (Section 12)

## How to Use

Apply the relevant section based on your current task:

| Task | Section |
|------|---------|
| Starting new work | Section 2 (Brainstorming) → Section 3 (Writing Plans) |
| Implementing a plan (this session) | Section 5 (Subagent-Driven Development) |
| Implementing a plan (separate session) | Section 4 (Executing Plans) |
| Multiple independent problems | Section 6 (Dispatching Parallel Agents) |
| Writing or fixing code | Section 7 (Test-Driven Development) |
| Bug, test failure, unexpected behavior | Section 8 (Systematic Debugging) |
| About to claim work is done | Section 9 (Verification Before Completion) |
| After completing work | Section 10 (Code Review) |
| Need isolated workspace | Section 11 (Using Git Worktrees) |
| Ready to merge/integrate | Section 12 (Finishing a Development Branch) |
| Creating new skills | Section 13 (Writing Skills) |

**Skill priority:** Process skills first (brainstorming, debugging), then implementation skills.

**Skill types:**
- **Rigid** (TDD, debugging, verification): Follow exactly. Don't adapt away discipline.
- **Flexible** (patterns, worktrees): Adapt principles to context.

---

## 1. Using Superpowers

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

**Rule:** Invoke relevant skills BEFORE any response or action. Even a 1% chance a section might apply means you should check.

**Process:**
1. User message received
2. Check: might any section apply?
   - Yes → Follow that section
   - No → Respond directly
3. If about to plan: check Section 2 (Brainstorming) first
4. If section has checklist: create todo per checklist item
5. Announce: "Using [skill] to [purpose]"

**Priority order:**
1. Process sections first (brainstorming, debugging)
2. Implementation sections second

**User instructions say WHAT, not HOW.** "Add X" or "Fix Y" doesn't mean skip workflows.

### Red Flags — You're Rationalizing

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

---

## 2. Brainstorming

**Use before:** Any creative work — creating features, building components, adding functionality, or modifying behavior.

<HARD-GATE>
Do NOT write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

### Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

### Checklist

1. **Explore project context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to complexity, get user approval after each section
5. **Write design doc** — save to `docs/plans/YYYY-MM-DD-<topic>-design.md` and commit
6. **Transition to implementation** — follow Section 3 (Writing Plans)

### Process

- Ask one question at a time. Prefer multiple choice.
- Propose 2-3 approaches with trade-offs. Lead with your recommendation.
- Present design sections incrementally. Get approval after each.
- Cover: architecture, components, data flow, error handling, testing.
- Apply YAGNI ruthlessly.
- Be flexible — go back and clarify when something doesn't make sense.

### After Design Approval

Write validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`, commit, then follow Section 3 (Writing Plans).

**The terminal state is invoking writing-plans.** Do NOT invoke any other implementation skill. The ONLY next step after brainstorming is writing-plans.

### Key Principles

- **One question at a time** — Don't overwhelm with multiple questions
- **Multiple choice preferred** — Easier to answer than open-ended when possible
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design, get approval before moving on

---

## 3. Writing Plans

**Use when:** You have a spec or requirements for a multi-step task, before touching code.

Write comprehensive implementation plans with bite-sized tasks. Assume the implementer has zero context. Document exact file paths, complete code, exact commands with expected output.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`

### Plan Header Template

Every plan MUST start with:

    # [Feature Name] Implementation Plan
    > **For agent:** REQUIRED SUB-SKILL: Use Section 4 or Section 5 to implement this plan.
    **Goal:** [One sentence]
    **Architecture:** [2-3 sentences]
    **Tech Stack:** [Key technologies]

### Task Granularity

Each step is one action (2-5 minutes):
- "Write the failing test" — step
- "Run it to verify it fails" — step
- "Implement minimal code to pass" — step
- "Run tests to verify pass" — step
- "Commit" — step

### Task Structure

    ### Task N: [Component Name]
    **Files:**
    - Create: `exact/path/to/file.py`
    - Modify: `exact/path/to/existing.py:123-145`
    - Test: `tests/exact/path/to/test.py`
    **Step 1:** Write failing test (with complete code)
    **Step 2:** Run test, verify fails (exact command + expected output)
    **Step 3:** Write minimal implementation (complete code)
    **Step 4:** Run test, verify passes (exact command + expected output)
    **Step 5:** Commit (exact git commands)

### Remember

- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

### Execution Handoff

After saving plan, offer:

**"Plan complete and saved. Two execution options:**

**1. Subagent-Driven (this session)** — fresh subagent per task, review between tasks, fast iteration → follow Section 5

**2. Parallel Session (separate)** — open new session, batch execution with checkpoints → follow Section 4

**Which approach?"**

---

## 4. Executing Plans

**Use when:** You have a written implementation plan to execute in a separate session with review checkpoints.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

### Process

1. **Load and review plan** — Read critically, raise concerns before starting. If no concerns: create task list and proceed.
2. **Execute batch** — Default first 3 tasks. For each: mark in_progress → follow steps exactly → run verifications → mark completed
3. **Report** — Show what was implemented, verification output. Say: "Ready for feedback."
4. **Continue** — Apply feedback, execute next batch, repeat
5. **Complete** — After all tasks verified, follow Section 12 (Finishing a Development Branch)

### When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker mid-batch (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

### When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** — stop and ask.

### Rules

- Follow plan steps exactly
- Don't skip verifications
- Between batches: report and wait
- Stop when blocked, don't guess
- Never start implementation on main/master without explicit consent

### Integration

- REQUIRED: Set up workspace with Section 11 (Git Worktrees) before starting
- After all tasks: follow Section 12 (Finishing a Development Branch)

---

## 5. Subagent-Driven Development

**Use when:** Executing implementation plans with independent tasks in the current session. Fresh subagent per task + two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

### Process

1. **Read plan, extract all tasks** with full text and context. Create task list.
2. **Per task:**
   a. Dispatch implementer subagent (provide full task text + context, don't make them read plan file)
   b. If subagent asks questions → answer clearly before proceeding
   c. Subagent implements, tests, commits, self-reviews
   d. Dispatch spec reviewer subagent → verify code matches spec
   e. If issues → implementer fixes → re-review until ✅
   f. Dispatch code quality reviewer subagent
   g. If issues → implementer fixes → re-review until ✅
   h. Mark task complete
3. **After all tasks:** Dispatch final code reviewer for entire implementation
4. **Complete:** Follow Section 12 (Finishing a Development Branch)

### Implementer Subagent Prompt

Provide: full task text, context (where it fits), working directory. Tell them:
- Implement exactly what task specifies
- Write tests (TDD if task says to)
- If you have questions about requirements, approach, or anything unclear — **ask them now before starting**
- Commit work
- Self-review: completeness (all requirements?), quality (clean, maintainable?), discipline (YAGNI?), testing (real behavior, not mocks?)
- If you find issues during self-review, fix them now before reporting
- Report: what implemented, test results, files changed, self-review findings, concerns

### Spec Reviewer Prompt

Provide: full task requirements, implementer's report. Tell them:
- **CRITICAL: Do NOT trust the implementer's report** — read actual code
- The implementer may be incomplete, inaccurate, or optimistic
- Check by reading code: missing requirements, extra/unneeded work, misunderstandings
- Report: ✅ spec compliant or ❌ issues with file:line references

### Code Quality Reviewer Prompt

Use code review template (see Section 10). Provide: BASE_SHA, HEAD_SHA, description.
- Only dispatch after spec compliance passes
- Returns: Strengths, Issues (Critical/Important/Minor), Assessment

### Rules

- Never start on main/master without consent
- Never skip reviews (spec OR quality)
- Spec review BEFORE code quality review
- Don't dispatch parallel implementation subagents (conflicts)
- Don't move to next task with open review issues
- If subagent fails → dispatch fix subagent, don't fix manually (context pollution)
- Don't make subagent read plan file (provide full text instead)
- Accept "close enough" on spec compliance → NOT acceptable (spec issues = not done)
- **Start code quality review before spec compliance is ✅** → WRONG ORDER

---

## 6. Dispatching Parallel Agents

**Use when:** 2+ independent tasks that can be worked on without shared state or sequential dependencies.

### When to Use

- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need full system context to understand
- Agents would interfere (editing same files, shared resources)
- Exploratory debugging (you don't know what's broken yet)

### Pattern

1. **Identify independent domains** — group failures by what's broken
2. **Create focused agent tasks** — each gets: specific scope, clear goal, constraints, expected output format
3. **Dispatch in parallel** — one agent per domain
4. **Review and integrate** — read summaries, verify no conflicts, run full test suite

### Agent Prompt Structure

Good prompts are: focused (one problem domain), self-contained (all context needed), specific about output (what to return).

- ❌ Too broad: "Fix all the tests" — agent gets lost
- ✅ Specific: "Fix agent-tool-abort.test.ts — 3 failures listed below"
- ❌ No constraints: agent might refactor everything
- ✅ Constrained: "Do NOT change production code" or "Fix tests only"
- ❌ Vague output: "Fix it" — you don't know what changed
- ✅ Specific: "Return summary of root cause and changes"

### Real Example

**Scenario:** 6 test failures across 3 files after major refactoring

**Dispatch:**
- Agent 1 → Fix agent-tool-abort.test.ts (3 timing issues)
- Agent 2 → Fix batch-completion-behavior.test.ts (2 event structure bugs)
- Agent 3 → Fix tool-approval-race-conditions.test.ts (1 async issue)

**Results:** All fixes independent, no conflicts, full suite green. 3 problems solved in time of 1.

---

## 7. Test-Driven Development

**Use when:** Implementing any feature or bugfix, before writing implementation code.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

### The Iron Law

    NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

Write code before the test? Delete it. Start over. No exceptions:
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

### RED — Write Failing Test

Write one minimal test showing what should happen.

**Good:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };
  const result = await retryOperation(operation);
  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing.

**Bad:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(2);
});
```
Vague name, tests mock not code.

**Requirements:** One behavior. Clear name. Real code (no mocks unless unavoidable).

### Verify RED

**MANDATORY. Never skip.**

Run test. Confirm: fails (not errors), expected failure message, fails because feature missing.

- Test passes? You're testing existing behavior. Fix test.
- Test errors? Fix error, re-run until it fails correctly.

### GREEN — Minimal Code

Write simplest code to pass the test. Don't add features, refactor, or "improve" beyond the test.

**Good:** Just enough to pass.
**Bad:** Over-engineered with options/backoff/callbacks the test doesn't require (YAGNI).

### Verify GREEN

**MANDATORY.**

Run test. Confirm: passes, other tests still pass, output pristine (no errors, warnings).

- Test fails? Fix code, not test.
- Other tests fail? Fix now.

### REFACTOR

After green only: remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

### Why Order Matters

**"I'll write tests after"** — Tests written after code pass immediately. Passing immediately proves nothing: might test wrong thing, might test implementation not behavior, might miss edge cases. Test-first forces you to see the test fail, proving it actually tests something.

**"Already manually tested"** — Manual testing is ad-hoc. No record, can't re-run, easy to forget cases. Automated tests are systematic.

**"Deleting X hours is wasteful"** — Sunk cost fallacy. The time is already gone. Keeping unverified code is technical debt.

**"TDD is dogmatic"** — TDD IS pragmatic: finds bugs before commit, prevents regressions, documents behavior, enables refactoring. "Pragmatic" shortcuts = debugging in production = slower.

### Bug Fix Example

**Bug:** Empty email accepted

**RED:**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED:** FAIL — expected 'Email required', got undefined ✓

**GREEN:**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) return { error: 'Email required' };
  // ...
}
```

**Verify GREEN:** PASS ✓ → **REFACTOR** → extract validation if needed.

### Verification Checklist

Before marking work complete:
- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

### When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

### Testing Anti-Patterns

When adding mocks or test utilities, avoid these pitfalls:
- **Testing mock behavior instead of real behavior** — Assert on real component output, not mock existence
- **Adding test-only methods to production classes** — Move to test utilities instead
- **Mocking without understanding dependencies** — Understand side effects before mocking; mock at lowest level needed
- **Incomplete mocks** — Mock the COMPLETE data structure as it exists in reality
- **Tests as afterthought** — Testing is part of implementation, not optional follow-up

### Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is debt. |
| "Keep as reference" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD faster than debugging. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |
| "It's about spirit not ritual" | Violating the letter IS violating the spirit. |

### Red Flags — STOP and Start Over

Code before test. Test after implementation. Test passes immediately. Can't explain why test failed. Rationalizing "just this once." "I already manually tested it." "Keep as reference." "This is different because..."

**All mean: Delete code. Start over with TDD.**

---

## 8. Systematic Debugging

**Use when:** Any bug, test failure, or unexpected behavior — before proposing fixes.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

### The Iron Law

    NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

If you haven't completed Phase 1, you cannot propose fixes.

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- You don't fully understand the issue

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read error messages carefully** — don't skip. Read stack traces completely. Note line numbers, file paths, error codes.
2. **Reproduce consistently** — exact steps, every time. Not reproducible → gather more data, don't guess.
3. **Check recent changes** — git diff, recent commits, new dependencies, config changes, environmental differences.
4. **Gather evidence in multi-component systems** — Log data at each component boundary. Run once to see WHERE it breaks. Then investigate that component.

   Example: For CI → build → signing pipeline:
   ```bash
   # Log at each layer boundary:
   # Layer 1 (workflow): echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"
   # Layer 2 (build): env | grep IDENTITY
   # Layer 3 (signing): security find-identity -v
   # Reveals: which layer the propagation fails
   ```

5. **Trace data flow** — Where does bad value originate? Trace up the call stack to the source. Fix at source, not symptom.

   **Root cause tracing technique:** Observe symptom → find immediate cause → ask "what called this?" → keep tracing up → find original trigger → fix at source.

   Example: `git init` in wrong directory → `cwd: ''` → `createWorktree('')` → `Session.create()` → test accessed `tempDir` before `beforeEach` → **root cause**: top-level variable initialization.

### Phase 2: Pattern Analysis

1. Find working examples of similar code in the codebase
2. Compare: what's different between working and broken?
3. List every difference, however small
4. Understand dependencies and assumptions

### Phase 3: Hypothesis and Testing

1. Form single hypothesis: "X is root cause because Y"
2. Make SMALLEST possible change to test it
3. One variable at a time
4. Didn't work → new hypothesis. DON'T add more fixes on top.

### Phase 4: Implementation

1. Create failing test reproducing the bug (Section 7: TDD)
2. Implement single fix addressing root cause
3. Verify: test passes, no other tests broken
4. **If 3+ fixes failed:** STOP. Question the architecture. Discuss with your human partner.

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere

   This is NOT a failed hypothesis — this is a wrong architecture.

### Supporting Techniques

- **Defense-in-depth:** After finding root cause, validate at EVERY layer data passes through. Entry point → business logic → environment guards → debug instrumentation. Single validation can be bypassed; multiple layers make the bug structurally impossible.
- **Condition-based waiting:** Replace arbitrary timeouts/sleeps with condition polling. Wait for the actual condition, not a guess about timing. `waitFor(() => condition())` instead of `setTimeout(check, 500)`.

### Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too. |
| "Emergency, no time" | Systematic is FASTER than thrashing. |
| "Just try this first" | First fix sets the pattern. Do it right. |
| "I see the problem" | Seeing symptoms ≠ understanding root cause. |
| "Multiple fixes saves time" | Can't isolate what worked. Causes new bugs. |
| "One more fix attempt" (after 2+) | 3+ failures = architectural problem. Question pattern. |
| "Reference too long, I'll adapt" | Partial understanding guarantees bugs. Read completely. |

### Red Flags — STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- Proposing solutions before tracing data flow
- "I don't fully understand but this might work"
- Each fix reveals new problem in different place
- 3+ fix attempts failed → **question the architecture**

**ALL of these mean: STOP. Return to Phase 1.**

---

## 9. Verification Before Completion

**Use when:** About to claim work is complete, fixed, or passing — before committing or creating PRs.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

### The Iron Law

    NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

If you haven't run the verification command in this message, you cannot claim it passes.

### The Gate

Before claiming ANY status:

    1. IDENTIFY: What command proves this claim?
    2. RUN: Execute the FULL command (fresh, complete)
    3. READ: Full output, check exit code, count failures
    4. VERIFY: Does output confirm the claim?
       - If NO: State actual status with evidence
       - If YES: State claim WITH evidence
    5. ONLY THEN: Make the claim

    Skip any step = lying, not verifying

### What Counts as Verification

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build: exit 0 | Linter passing |
| Bug fixed | Test original symptom | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

### Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

### Red Flags

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- Trusting agent success reports
- Relying on partial verification
- ANY wording implying success without having run verification

**Run the command. Read the output. THEN claim the result.**

### Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

---

## 10. Code Review

**Use when:** Completing tasks, implementing major features, before merging, or when receiving review feedback.

### Part 1: Requesting Review

**Mandatory after:** each task in subagent-driven development, major features, before merge.

**How to request:**
1. Get git SHAs: `BASE_SHA=$(git rev-parse HEAD~1)`, `HEAD_SHA=$(git rev-parse HEAD)`
2. Dispatch code-reviewer subagent with the template below
3. Act on feedback: fix Critical immediately, fix Important before proceeding, note Minor for later

**Code Reviewer Template:**

    You are reviewing code changes for production readiness.
    Review {WHAT_WAS_IMPLEMENTED} against {PLAN_OR_REQUIREMENTS}.
    Git range: {BASE_SHA}..{HEAD_SHA}

    Check: code quality, architecture, testing, requirements, production readiness.

    Review Checklist:
    - Code: separation of concerns, error handling, type safety, DRY, edge cases
    - Architecture: design decisions, scalability, performance, security
    - Testing: tests test logic not mocks, edge cases, integration tests, all passing
    - Requirements: all met, matches spec, no scope creep, breaking changes documented

    Output format:
    ### Strengths — what's well done (be specific, file:line)
    ### Issues
    #### Critical (Must Fix) — bugs, security, data loss
    #### Important (Should Fix) — architecture, missing features, test gaps
    #### Minor (Nice to Have) — style, optimization
    For each: file:line, what's wrong, why it matters, how to fix
    ### Assessment — Ready to merge? [Yes/No/With fixes]

### Part 2: Receiving Feedback

**Response pattern:** READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT

**Forbidden responses — NEVER say:**
- "You're absolutely right!" (performative)
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**Instead:** Restate the technical requirement, ask clarifying questions, push back if wrong, or just fix it.

**Handling unclear feedback:**
```
IF any item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on ALL unclear items
  WHY: Items may be related. Partial understanding = wrong implementation.
```

**Implementation order for multi-item feedback:**
1. Clarify anything unclear FIRST
2. Blocking issues (breaks, security)
3. Simple fixes (typos, imports)
4. Complex fixes (refactoring, logic)
5. Test each fix individually

**YAGNI check:** If reviewer suggests "implementing properly," grep codebase for actual usage. If unused → "This endpoint isn't called. Remove it (YAGNI)?"

**When to push back:**
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Conflicts with architectural decisions

**When feedback IS correct:**
```
✅ "Fixed. [Brief description]"
✅ [Just fix it in code]
❌ "You're absolutely right!" / "Thanks for catching that!"
```

Actions speak. Just fix it.

---

## 11. Using Git Worktrees

**Use when:** Starting feature work that needs isolation or before executing implementation plans.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

### Directory Selection (priority order)

1. **Check existing:** `ls -d .worktrees 2>/dev/null` (preferred) or `ls -d worktrees 2>/dev/null`
   - If found: use that directory. If both exist, `.worktrees` wins.
2. **Check AGENTS.md:** `grep -i "worktree.*director" AGENTS.md 2>/dev/null`
   - If preference specified: use without asking.
3. **Ask user:** `.worktrees/` (project-local, hidden) or `~/.config/superpowers/worktrees/<project>/` (global)

### Safety Verification

For project-local directories: verify directory is in `.gitignore` before creating worktree.

    git check-ignore -q .worktrees 2>/dev/null

If NOT ignored:
1. Add appropriate line to `.gitignore`
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to repository.

### Creation Steps

1. **Detect project:** `project=$(basename "$(git rev-parse --show-toplevel)")`
2. **Create worktree:** `git worktree add "$path" -b "$BRANCH_NAME"`
3. **Run project setup** (auto-detect):
   ```bash
   if [ -f package.json ]; then npm install; fi
   if [ -f Cargo.toml ]; then cargo build; fi
   if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
   if [ -f pyproject.toml ]; then poetry install; fi
   if [ -f go.mod ]; then go mod download; fi
   ```
4. **Verify clean baseline** — run tests. If tests fail: report failures, ask whether to proceed.
5. **Report:** location, test results, ready status

### Rules

- Never create worktree without verifying it's ignored (project-local)
- Never skip baseline test verification
- Never proceed with failing tests without asking
- Follow directory priority: existing → AGENTS.md → ask
- Auto-detect setup commands from project files

---

## 12. Finishing a Development Branch

**Use when:** Implementation is complete, all tests pass, ready to integrate.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

### Process

1. **Verify tests pass** — if failing, stop. Cannot proceed.
2. **Determine base branch** — `git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null`
3. **Present exactly 4 options:**
   ```
   Implementation complete. What would you like to do?
   1. Merge back to <base-branch> locally
   2. Push and create a Pull Request
   3. Keep the branch as-is
   4. Discard this work
   ```
4. **Execute choice**
5. **Cleanup worktree** (for options 1, 2, 4 only)

### Option Details

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | Yes | - | - | Yes |
| 2. Create PR | - | Yes | Yes | - |
| 3. Keep as-is | - | - | Yes | - |
| 4. Discard | - | - | - | Yes (force) |

**Option 1 (Merge):** Checkout base → pull latest → merge feature → verify tests on merged result → delete feature branch → cleanup worktree

**Option 2 (Push/PR):** Push branch → `gh pr create` with summary and test plan → cleanup worktree

**Option 4 (Discard):** Require typed "discard" confirmation. Show what will be deleted (branch, commits, worktree). Then: checkout base → `git branch -D` → cleanup worktree

### Rules

- Never proceed with failing tests
- Always verify tests on merged result (option 1)
- Require typed "discard" confirmation (option 4)
- Don't force-push without explicit request
- Present exactly 4 options — don't use open-ended questions

---

## 13. Writing Skills

**Use when:** Creating new skills, editing existing skills, or verifying skills work.

### What is a Skill?

A reusable reference guide for proven techniques, patterns, or tools. NOT narratives about how you solved a problem once.

**Skills are:** Reusable techniques, patterns, tools, reference guides
**Skills are NOT:** One-off solutions, project-specific conventions, mechanical constraints (automate those instead)

### The Iron Law (Same as TDD)

    NO SKILL WITHOUT A FAILING TEST FIRST

Test with subagent pressure scenarios. Watch agents fail without skill (RED). Write minimal skill (GREEN). Close loopholes (REFACTOR).

### SKILL.md Structure

    ---
    name: skill-name-with-hyphens
    description: "Use when [specific triggering conditions]"
    ---

Sections: Overview → When to Use → Core Pattern → Quick Reference → Common Mistakes

### Description Field (Critical for Discovery)

**CRITICAL: Description = When to Use, NOT What the Skill Does**

Agents read description to decide which skills to load. The description should ONLY describe triggering conditions. Do NOT summarize the skill's process or workflow.

**Why:** Testing revealed that when a description summarizes workflow, agents follow the description shortcut instead of reading the full skill. A description saying "code review between tasks" caused an agent to do ONE review, even though the skill specified TWO reviews (spec + quality).

```yaml
# ❌ BAD: Summarizes workflow — agent may follow this instead of reading skill
description: Use when executing plans - dispatches subagent per task with code review

# ✅ GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks
```

### Naming

- Verb-first, active voice: `condition-based-waiting` not `async-test-helpers`
- Gerunds work well: `creating-skills`, `testing-skills`
- Name by what you DO: `root-cause-tracing` not `debugging-techniques`

### Key Rules

- One excellent example beats many mediocre ones
- Flowcharts only for non-obvious decisions
- Keep inline unless reference >100 lines
- Test BEFORE deploying. No exceptions.

### Bulletproofing Against Rationalization

Skills that enforce discipline need to resist rationalization:

1. **Close every loophole explicitly** — Don't just state the rule; forbid specific workarounds ("Don't keep it as reference, don't adapt it, delete means delete")
2. **Address "spirit vs letter"** — Add "Violating the letter IS violating the spirit" early
3. **Build rationalization table** — Capture every excuse agents make, add counters
4. **Create red flags list** — Make it easy to self-check when rationalizing

### Skill Creation Checklist

**RED:** Create pressure scenarios → run WITHOUT skill → document baseline failures (exact rationalizations agents use)
**GREEN:** Write skill addressing specific failures → run WITH skill → verify compliance
**REFACTOR:** Find new rationalizations → add counters → re-test until bulletproof

### Common Rationalizations for Skipping Testing

| Excuse | Reality |
|--------|---------|
| "Skill is obviously clear" | Clear to you ≠ clear to agents. Test it. |
| "It's just a reference" | References can have gaps. Test retrieval. |
| "Testing is overkill" | Untested skills always have issues. 15 min saves hours. |
| "I'll test if problems emerge" | Problems = agents can't use skill. Test BEFORE deploying. |
| "No time to test" | Deploying untested skill wastes more time fixing later. |
