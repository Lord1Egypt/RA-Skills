# Build Integration

The build and debug cycle transforms expert knowledge into executable project code and verifies it meets quality standards.

## Build Trigger (Phase 6)

### Input

The project-builder agent reads:

1. **Domain spec**: `domains/<domain_id>.json` — what the project is about
2. **Expert forum index**: `forum_index.json` — available experts
3. **Expert profiles**: `experts/*/profile.json` — detailed knowledge lenses
4. **Scoring report**: latest `scoring_reports/*.json` — what needs improvement
5. **Gap analysis**: latest `gap_analyses/*.json` — specific weaknesses

### Expert Lens Injection

For each expert in the council, inject their reasoning as build guidance:

```
For expert {name}:
- Core questions: {reasoning_kernel.core_questions}
- Preferred abstractions: {reasoning_kernel.preferred_abstractions}
- Anti-patterns: {advantage_knowledge_base.anti_patterns}
- Best used for: {domain_relevance.best_used_for}
```

The builder uses these lenses to:
- Choose architecture patterns that align with expert preferences
- Avoid anti-patterns identified by the council
- Prioritize implementation of features that address scoring gaps
- Structure code in ways that experts would find reviewable

### Build Output

The builder produces:
1. Project source code at the target repo path
2. Configuration files (package.json, pyproject.toml, etc.)
3. Test files (guided by expert testing preferences)
4. Documentation (guided by expert communication styles)
5. Build log at `build_logs/<timestamp>.log`

### Language/Framework Detection

The builder detects the target language and framework from:

1. Existing files in the target repo (if not empty)
2. Expert `advantage_knowledge_base.favorite_benchmarks` hints
3. Domain conventions (e.g., ML → Python, web → TypeScript)
4. Default: Python with standard project layout

## Debug Cycle (Phase 7)

The debug cycle follows a 6-stage verification loop. Each stage must pass before the artifact moves to RESCORE.

### Stage 1: Build Verification

```bash
# Auto-detect build command from project type
Python: python -m build / pip install -e .
TypeScript: npm run build / pnpm build
Go: go build ./...
Rust: cargo build
```

**On failure**:
- Extract error messages
- Tag with impacted axis (primarily `thickness`)
- Feed back to project-builder for targeted fix
- Max 3 retries per build error

### Stage 2: Type Check

```bash
Python: mypy . --strict
TypeScript: tsc --noEmit
Go: go vet ./...
Rust: cargo check
```

**On failure**:
- Extract type errors
- Tag with impacted axis (primarily `depth`)
- Fix type annotations or adjust types
- Max 3 retries

### Stage 3: Lint

```bash
Python: ruff check . / flake8
TypeScript: eslint .
Go: golint / staticcheck
Rust: cargo clippy
```

**On failure**:
- Extract lint warnings
- Auto-fix where possible
- Tag with impacted axis (primarily `depth`)
- Max 2 retries (lint issues are usually straightforward)

### Stage 4: Test Suite

```bash
Python: pytest --tb=short
TypeScript: npm test / vitest
Go: go test ./...
Rust: cargo test
```

**On failure**:
- Categorize failures by which expert domain they relate to
- Route failures to the appropriate expert lens for analysis
- Fix implementation or adjust test expectations
- Tag with impacted axis (primarily `thickness` and `effectiveness`)
- Max 3 retries

### Stage 5: Security Scan

```bash
# Check for common vulnerabilities
- Hardcoded secrets (API keys, passwords, tokens)
- SQL injection patterns
- XSS patterns
- Path traversal patterns
- Dependency vulnerabilities
```

**On failure**:
- Block immediately (security is CRITICAL)
- Fix the vulnerability
- Tag with impacted axis (`effectiveness` — insecure solutions are not effective)
- No retry limit — must fix all security issues

### Stage 6: Diff Review

Review changes since last iteration for:
- Regressions (features that worked before but now break)
- Scope creep (changes beyond what the scoring report recommended)
- Code quality degradation
- Missing tests for new code

**On failure**:
- Revert problematic changes
- Tag with impacted axis (varies)
- Max 2 retries

## Failure-to-Axis Mapping

| Failure Type | Primary Axis | Secondary Axis |
|-------------|-------------|----------------|
| Build failure | thickness | breadth |
| Type error | depth | thickness |
| Lint warning | depth | — |
| Test failure | thickness | effectiveness |
| Security issue | effectiveness | — |
| Regression | effectiveness | breadth |

## Build Log Format

Each build attempt is logged at `build_logs/<timestamp>.log`:

```json
{
  "timestamp": "2026-01-01T00:00:00Z",
  "iteration": 3,
  "phase": "build",
  "command": "npm run build",
  "exit_code": 0,
  "stdout": "...",
  "stderr": "...",
  "duration_seconds": 45,
  "stages": [
    { "name": "build", "status": "pass", "duration_seconds": 12 },
    { "name": "type_check", "status": "pass", "duration_seconds": 5 },
    { "name": "lint", "status": "pass", "duration_seconds": 3 },
    { "name": "test", "status": "fail", "failures": 2, "duration_seconds": 25 },
    { "name": "security", "status": "pass", "duration_seconds": 8 },
    { "name": "diff", "status": "pass", "duration_seconds": 2 }
  ]
}
```

## Expert Code Review

After DEBUG passes all stages, the expert council reviews the code:

1. Each expert applies their `critique_style` to the codebase
2. Each expert checks for their known `blind_spots` (does the code fall into patterns this expert would miss?)
3. Each expert evaluates against their `reasoning_kernel.failure_taxonomy` (does the code exhibit failure modes this expert detects quickly?)
4. The forum-moderator synthesizes all reviews into actionable feedback for the next BUILD phase

This expert code review is NOT a gate (it doesn't block progress) but it feeds into the RESCORE phase, where the maturity scorer considers expert satisfaction with the code quality.
