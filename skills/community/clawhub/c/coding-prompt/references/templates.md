## 4. Workflow Templates

Structured templates for each phase of feature development. Use directly or adapt.
For Weak → Strong transformation examples aligned with specific situations, see also `references/anti-patterns.md`.

### 4.1 Launch — Starting a New Feature

```
## Task: <feature name>

### Background
<1-2 sentences. What is the project, where does this feature fit?>

### Requirement (user-facing, no tech details)
<What the user will experience>

### Constraints (violations require rewrite)
- <tech constraint> — e.g., No extra AI models, reuse existing LLM
- <architecture constraint> — e.g., Python scripts do pure computation only
- <prohibition> — e.g., Must NOT hardcode matching rules

### Deliverable Standard
- <code quality> — e.g., English comments
- <documentation> — e.g., International docs in English
- <non-code artifacts> — e.g., SKILL.md follows same language standard

### Design Style
<one sentence> — e.g., Minimal but not rough, prefer reusing existing modules

### Execution
Give me a solution overview first (no code). I'll confirm the direction before implementation begins.
```

### 4.2 Confirm — Align Before Coding

```
Before writing code, provide:
1. Solution overview (2-3 sentences)
2. Files and modules affected (new vs. modified)
3. Key design decisions and rationale
4. Potential risks

I'll confirm before you start implementing.
```

**Skip this for**: single-function changes, parameter additions, trivial fixes.

### 4.3 Correct — Course Correction

```
The current implementation of <method/module> uses <approach>, which doesn't meet requirements.

Must NOT: <specific prohibition>
Reason: <one sentence>

Should be: <correct direction or principle>
Reference: <analogy if available, e.g., "similar to how X handles this">

Check current code:
- If compliant: explain where
- If not: modify and report which files/functions changed
```

**Minimum change principle**: Only touch code directly related to the current requirement. Do not refactor unrelated code. Do not add unrequested features.

### 4.4 Continue — Long Task Progression

| Situation | Prompt |
|-----------|--------|
| Clear direction, low risk | `继续。` |
| Recommended (prevent drift) | `继续，下一步是 <step>。遇到阻碍告诉我，不要自作主张改变方向。` |
| Long task, batch execution | `已完成：<done parts>。本轮只做：<this round's goal>。其余等我确认后继续。` |

### 4.5 Verify — Testing & Acceptance

```
Test <module/feature> and generate a test report.

Testing requirements:
- Coverage: <core features list>
- Method: Real execution (not mock), verify actual output
- Edge cases: Boundary conditions and error scenarios
- Environment issues: Don't stop on display errors; skip and report at end

Report requirements:
- Format: Markdown
- Content: Test cases / Results / Pass/Fail / Issue analysis / Improvement suggestions
- Filename: <module>_test_report.md
- End with one-sentence summary: Is this ready for production?
```

### 4.6 Review — Code Review

```
Review <file/module>, focus on:
1. Hardcoded logic that shouldn't be hardcoded
2. Duplicate code or redundant imports
3. Deprecated API usage
4. Error handling completeness
5. Project constraint compliance: <one-line constraint>

Classify issues: P0 (must fix) / P1 (should fix) / P2 (nice to have).
```
