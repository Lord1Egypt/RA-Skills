---
name: dev-test
description: "Structured development and testing SOP for implementing code changes. Covers codebase study, minimal focused implementation, test writing patterns, test execution, and diff review. Applies to any development work — bug fixes, features, refactors, or open-source contributions. Use when you need a disciplined development workflow with built-in quality checks."
---

# Dev Test — Development & Testing SOP

## Overview

A structured workflow for implementing code changes with quality built in. Covers the full cycle from understanding the codebase to having a verified, reviewable diff.

**Use cases**: Bug fixes, feature development, refactoring, open-source contributions, any code change that needs to be correct and maintainable.

## Workflow

### Phase 1: Study Before Coding

**Never write code before understanding the context.** This phase prevents wasted effort and bad designs.

#### 1a. Understand the project conventions

Check for and read these files (if they exist):
- `CONTRIBUTING.md` — contribution guidelines
- `.editorconfig` — formatting rules
- `pyproject.toml` / `package.json` / `Makefile` — project config, linting, formatting
- `tox.ini` / `.flake8` / `.eslintrc` — code style rules

#### 1b. Study the area of change

- Read the module(s) you'll be modifying
- Trace the execution path around the bug/feature
- Understand data flow: what goes in, what comes out
- Note dependencies: what other modules interact with this code

#### 1c. Study existing tests

- Find the test directory structure: `tests/`, `__tests__/`, `test/`
- Note the test framework: pytest, jest, go test, JUnit, etc.
- Study naming conventions: `test_feature.py`, `feature.test.ts`, `feature_test.go`
- Note fixture/setup patterns used
- Check for test utilities, factories, or mocks

#### 1d. Draft a mental model

Before writing code, articulate:
- **What** needs to change (specific behavior)
- **Where** in the code (files, functions, classes)
- **How** you'll change it (approach)
- **What could go wrong** (edge cases, regressions)

### Phase 2: Implement

#### Core principles

1. **Minimal, focused changes**
   - Fix the bug / add the feature. Nothing else.
   - Avoid unrelated formatting changes, import reordering, or drive-by refactors.
   - If you spot something else to fix, note it for a separate commit/PR.

2. **Follow existing patterns**
   - Match the codebase's style, not your preferred style
   - Use the same naming conventions, indentation, comment style
   - If the project uses `snake_case`, don't introduce `camelCase`

3. **Add comments for non-obvious logic**
   - "Why" comments, not "what" comments
   - Explain trade-offs, workarounds, and intentional decisions

4. **Design for quality**

   | Principle | Meaning | Example |
   |-----------|---------|---------|
   | Defense-in-depth | Layer multiple protections | Validate input at API + service + DB layer |
   | Backward compatibility | Don't break existing behavior | Add new params with defaults |
   | Graceful degradation | Handle missing features | Platform-specific code falls back safely |
   | Extensibility | Prefer composable designs | Plugin/middleware over hardcoded switch |
   | Single responsibility | One function = one job | Extract logic instead of growing functions |

### Phase 3: Write Tests

#### Test categories (implement in order)

1. **Fix verification** — prove the bug is fixed / feature works
   ```
   test_feature_handles_null_input()        # The exact scenario from the issue
   ```

2. **Edge cases** — boundary conditions
   ```
   test_feature_with_empty_string()
   test_feature_with_max_length_input()
   test_feature_with_special_characters()
   ```

3. **Error handling** — invalid inputs, failure paths
   ```
   test_feature_raises_on_invalid_type()
   test_feature_returns_none_on_missing_key()
   ```

4. **Regression** — existing behavior preserved
   ```
   test_existing_behavior_unchanged()
   test_other_module_still_works()
   ```

#### Test writing guidelines

- **One assertion per test** (ideally) — makes failures easy to diagnose
- **Descriptive names** — `test_oauth_token_refreshes_when_expired` not `test_token`
- **Arrange-Act-Assert** pattern:
  ```python
  def test_feature():
      # Arrange
      input_data = create_test_data()

      # Act
      result = feature(input_data)

      # Assert
      assert result.status == "success"
  ```
- **Use fixtures** for reusable setup
- **Mock external dependencies** — network calls, file system, databases
- **Test behavior, not implementation** — don't assert on internal state

### Phase 4: Run Tests

#### Progressive testing strategy

```bash
# 1. Run only your new/modified tests first (fast feedback)
python -m pytest tests/test_my_feature.py -v --tb=short
# or: npm test -- --testPathPattern=my_feature
# or: go test ./pkg/my_feature/... -v

# 2. Run the full test module/directory
python -m pytest tests/ -v --tb=short

# 3. Run the entire test suite (before committing)
python -m pytest --tb=short
# or: npm test
# or: go test ./...
```

#### Handling test results

| Scenario | Action |
|----------|--------|
| All pass ✅ | Proceed to diff review |
| Your tests fail | Fix the code, re-run |
| Pre-existing failures | Note them, don't fix (out of scope) |
| Flaky tests (pass/fail randomly) | Run 3x to confirm flakiness, note in PR |
| Tests you can't run (need env/infra) | Note in PR, explain what you tested manually |

### Phase 5: Review the Diff

**Before committing, review every line of your diff.**

```bash
# Overview of what changed
git diff --stat

# Full diff
git diff

# If already staged
git diff --cached
```

#### Diff review checklist

- [ ] Every change is intentional (no accidental edits)
- [ ] No debug prints, TODO comments, or temporary code left in
- [ ] No secrets, tokens, or personal paths hardcoded
- [ ] No unrelated formatting changes
- [ ] All new functions/classes have appropriate docstrings/comments
- [ ] Test coverage looks adequate for the changes
- [ ] File additions are in the right directories

### Phase 6: Commit

```bash
# Stage specific files (never use `git add .`)
git add path/to/modified_file.py
git add tests/test_new_feature.py

# Verify staged files
git diff --cached --stat

# Commit with conventional message
git commit -m "fix(module): short description of what was fixed

Longer explanation of why, if non-obvious.

Addresses #issue_number"
```

#### Commit message format

```
{type}({scope}): {concise description}

{body: what and why, not how}

{footer: issue refs, test results, breaking changes}
```

| Type | When |
|------|------|
| `fix` | Bug fix |
| `feat` | New feature |
| `refactor` | Code restructure (no behavior change) |
| `test` | Adding/fixing tests only |
| `docs` | Documentation changes only |
| `chore` | Build/tooling/dependency changes |

## Output

- Committed code changes + tests on feature branch
- All tests passing
- Clean, reviewable diff

## Tips

- This skill works standalone for any development task.
- In a contribution pipeline, it follows **repo-setup** and feeds into **pr-pilot**.
- For large features, repeat Phase 2-5 in small increments rather than one big change.
- When pair-programming with AI: have the AI study the codebase (Phase 1) before asking it to implement anything.
