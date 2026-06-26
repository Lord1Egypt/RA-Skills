# Code Quality Reviewer Prompt Template

Dispatched ONLY after spec compliance passes. Checks the code is well-built.

## Template

```
You are reviewing code quality for a completed implementation.

## What Was Built

[Brief description from implementer's report]

## Changed Files

[List from implementer's report, or use git diff]

## Your Job

Review the actual code for quality. Focus on:

**Code Quality:**
- Clear, descriptive naming?
- Clean, readable structure?
- Follows existing codebase patterns and conventions?
- No dead code, unused imports, leftover debug statements?

**Testing:**
- Tests verify behavior, not implementation details?
- Tests comprehensive? Edge cases covered?
- Tests actually run and pass? (run them yourself)

**Safety:**
- Input validation at system boundaries?
- No hardcoded secrets, credentials, or PII?
- Error handling appropriate (not excessive)?

**Maintainability:**
- Would a new developer understand this code?
- No premature abstractions or over-engineering?
- Comments only where logic isn't self-evident?

## Severity Classification

- **Critical:** Must fix before merge. Security issues, data loss risk, broken functionality.
- **Important:** Should fix. Code smell, missing tests, unclear naming.
- **Minor:** Note for awareness. Style preferences, minor optimizations.

## Output Format

**Strengths:** [what's good about this implementation]

**Issues:**
- [Critical/Important/Minor]: [description] — [file:line]

**Assessment:** Ready to merge / Needs fixes / Needs discussion
```

## Usage with OpenClaw

```javascript
sessions_spawn({
  task: `[paste template above with filled placeholders]`,
  runtime: "subagent",
  model: "gpt",  // second opinion from different model family
  mode: "run",
  cwd: "/path/to/project"
})
```
