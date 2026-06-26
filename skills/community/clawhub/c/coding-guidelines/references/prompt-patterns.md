# Prompt Patterns for Coding

## Effective Prompt Structures

### The Intent-Constraint Pattern (most common, most effective)
```
[What you want] + [Why] + [Constraints]
```
Examples:
- "Add user authentication using JWT. We're on Express + MongoDB. Don't break the existing session middleware."
- "Refactor the payment module to support Stripe alongside PayPal. Keep the same interface so other modules don't change."
- "This endpoint is slow. Profile it and fix the bottleneck. It's called ~1000/min in production."

### The Example-Driven Pattern (for complex or ambiguous tasks)
```
[What you want] + [Example of desired output] + [Edge cases]
```
Example:
- "Generate API response wrappers. Here's what our successful responses look like: `{success: true, data: {...}}`. Errors should follow: `{success: false, error: {code: string, message: string}}`. Handle validation errors, auth errors, and not-found differently."

### The Exploration Pattern (when you don't know the approach)
```
[Problem statement] + [What you've tried/considered] + [What you need]
```
Example:
- "Our React app re-renders too often on the dashboard. I think it's the data fetching hook but not sure. Can you investigate and suggest the best fix?"

### The Review Pattern (for existing code)
```
[Code/scope to review] + [What to check for] + [Standards to apply]
```
Example:
- "Review the auth middleware in src/middleware/auth.ts. Check for security issues, edge cases with token expiry, and whether it follows our error handling pattern from src/utils/errors.ts."

## Anti-Patterns (what NOT to do)

### The Micromanagement Prompt
❌ "Create a file called user.ts. Import express. Create a router. Add a GET endpoint at /users. Query the database. Return JSON."
✅ "Add a GET /users endpoint. We use Express + Prisma. Follow the pattern in products.ts."

### The Vague Hope Prompt
❌ "Make the code better"
✅ "The error handling in the API routes is inconsistent — some return proper error responses, others just crash. Normalize them to use our error middleware."

### The Kitchen Sink Prompt
❌ Loading 20 files "for context" and asking to "refactor everything"
✅ "Refactor the auth module. It's spread across auth.ts, middleware.ts, and utils/auth-helpers.ts. Consolidate into a single auth/ directory with the same external interface."

### The Never-Ending Correction
❌ After 5 rounds of "almost, but fix this one thing"
✅ "That approach isn't working. Let me restate the goal: [clear goal]. Start fresh."

## Prompt Templates for Common Tasks

### Adding a Feature
```
Add [feature] to [module/app].
Tech stack: [stack]
Similar existing feature for reference: [file/endpoint]
Constraints: [don't break X, follow Y pattern, must support Z]
```

### Debugging
```
[What's happening] vs [What should happen]
Where: [file/component/endpoint]
I've already checked: [what you've ruled out]
Reproduction: [how to trigger it]
```

### Refactoring
```
Refactor [scope] to [goal].
Current problems: [pain points]
Must preserve: [external interfaces, tests, behavior]
Can change: [internal structure, naming, organization]
```

### Code Review
```
Review [scope].
Focus on: [security / performance / maintainability / correctness]
Standard: [our style guide / best practices for X]
Severity threshold: [flag everything / only critical issues]
```

## The Clarification Framework

When a prompt is ambiguous, use this priority order for questions:

1. **Goal** — What's the end state? (1 question)
2. **Scope** — How big is this? What's in/out? (1 question)
3. **Constraints** — What must not change? What must be followed? (1-2 questions)
4. **Approach** — Only if the user seems to want input on *how* (optional)

Max 3-4 questions. If you need more, the task probably needs a planning session, not a Q&A.

**Don't ask what you can discover.** Read the code first. Check the project structure. Look at existing patterns. Then ask only what you genuinely can't figure out.
