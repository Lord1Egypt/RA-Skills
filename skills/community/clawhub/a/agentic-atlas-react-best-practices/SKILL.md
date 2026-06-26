---
name: react-best-practices
description: |
  Audits React code for performance, bundle size, and best practices. Use when reviewing React code, auditing bundle size, finding performance issues, checking React 18+ patterns, or evaluating a React codebase.
  NOT for: non-React projects, backend Node.js code, or CSS-only reviews.
version: 1.0.0
author: asimons81
source: https://github.com/asimons81/Agentic-Atlas
tags: [react, performance, audit, bundle-size, frontend, code-quality]
agency_score: 7
---

# React Best Practices Skill

Audits React applications for performance, bundle size, and React 18+ best practices.

## Instructions

When reviewing or auditing React code:

1. Run the audit against the specified code or repository
2. Check against the 40+ auditable rules (see below)
3. Report findings with severity (error, warning, info)
4. Provide actionable fix suggestions with before/after code examples
5. For performance issues, identify the root cause and recommended optimization
6. For bundle issues, suggest code splitting or lazy loading strategies

## Auditable Rules (Sample)

### Performance
- `no-missing-deps`: Hook dependencies must be complete
- `avoid-inline-objects-in-jsx`: Inline objects cause unnecessary re-renders
- `prefer-useMemo`: Expensive computations should use useMemo
- `prefer-useCallback`: Callbacks passed to children should use useCallback

### React 18+
- `prefer-use client directive`: Server Components compliance
- `no-unnecessary-fragments`: Avoid unnecessary fragment wrappers
- `require-useTransition`: Long renders should use useTransition

### Bundle Size
- `no-bare-imports`: Use named imports over namespace imports
- `avoid-default-imports`: Default imports prevent tree shaking
- `check-duplicate-packages`: Duplicate package versions inflate bundle

### Accessibility
- `require-aria-labels`: Interactive elements need ARIA labels
- `require-keyboard-handlers`: Click handlers need keyboard equivalents

## Output Format

```json
{
  "file": "src/components/UserProfile.tsx",
  "rules": [
    {
      "rule": "no-missing-deps",
      "severity": "error",
      "line": 42,
      "message": "Missing dependency 'userId' in useEffect",
      "fix": "Add userId to dependency array"
    }
  ],
  "summary": { "errors": 2, "warnings": 5, "info": 1 }
}
```

## Example

```
User: "Audit our React codebase for performance issues"

→ Run audit → Report: 3 errors (missing deps, inline objects), 7 warnings → Provide fixes for each
```

## Dependencies

Requires: Node.js, project with React 16+ (for React 18+ rules, requires React 18+)
