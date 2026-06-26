---
name: code-review-assistant
description: Comprehensive code review assistant that analyzes code quality, identifies bugs, suggests improvements, and ensures adherence to best practices. Use when reviewing pull requests, analyzing code changes, or performing code quality audits.
license: MIT
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
metadata:
  version: "1.0.0"
  category: "Development"
  author: "Skills Example"
---

# Code Review Assistant

## Overview

This skill helps you perform thorough code reviews by analyzing code quality, identifying potential issues, and suggesting improvements. It follows industry best practices and can adapt to different programming languages and coding standards.

## Key Features

- **Security Analysis**: Identify common security vulnerabilities (SQL injection, XSS, CSRF, etc.)
- **Performance Review**: Detect performance bottlenecks and inefficient code patterns
- **Code Style**: Check adherence to coding conventions and best practices
- **Bug Detection**: Identify logical errors, edge cases, and potential bugs
- **Documentation**: Verify code documentation and suggest improvements
- **Test Coverage**: Analyze test quality and coverage

## Review Process

### 1. Initial Assessment

When reviewing code, start by understanding:
- What problem is being solved?
- What files are changed?
- What is the scope of changes?

### 2. Security Review

Check for common vulnerabilities:

**Input Validation**
- Validate all user inputs
- Sanitize data before use
- Check for injection vulnerabilities

**Authentication & Authorization**
- Verify proper access controls
- Check for authentication bypasses
- Ensure sensitive data protection

**Data Handling**
- Check for hardcoded credentials
- Verify secure data storage
- Review logging of sensitive information

### 3. Code Quality Review

**Readability**
- Clear variable and function names
- Appropriate comments for complex logic
- Consistent formatting and style

**Maintainability**
- DRY principle (Don't Repeat Yourself)
- Single Responsibility Principle
- Proper error handling

**Performance**
- Efficient algorithms and data structures
- Avoid unnecessary loops or computations
- Proper resource management (memory, connections)

### 4. Testing Review

**Test Coverage**
- Unit tests for critical functions
- Integration tests for workflows
- Edge cases and error conditions

**Test Quality**
- Clear test names describing what's tested
- Proper assertions
- Independent and repeatable tests

## Language-Specific Considerations

### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Proper exception handling with specific exception types
- Avoid mutable default arguments

### JavaScript/TypeScript
- Use const/let instead of var
- Proper async/await error handling
- TypeScript: leverage type system fully
- Avoid callback hell, use Promises

### Java
- Follow naming conventions (CamelCase)
- Proper exception handling
- Resource management with try-with-resources
- Thread safety considerations

### Go
- Follow Go idioms and conventions
- Proper error handling (don't ignore errors)
- Use defer for cleanup
- Context usage for cancellation

## Review Template

When providing review feedback, use this structure:

```markdown
## Code Review Summary

**Overall Assessment**: [Brief overview]

### 🔴 Critical Issues
- [Issue 1 with location and severity]
- [Issue 2 with location and severity]

### 🟡 Improvements Suggested
- [Suggestion 1 with reasoning]
- [Suggestion 2 with reasoning]

### 🟢 Positive Aspects
- [What was done well]
- [Good practices observed]

### 📝 Additional Notes
- [Any other observations or recommendations]
```

## Common Anti-Patterns to Watch For

### General
- Magic numbers (use named constants)
- Deep nesting (refactor for readability)
- God objects/classes (break into smaller components)
- Tight coupling (prefer dependency injection)

### Performance
- N+1 query problems
- Inefficient string concatenation in loops
- Memory leaks (unreleased resources)
- Synchronous operations blocking main thread

### Security
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Insecure direct object references
- Missing rate limiting

## Best Practices

1. **Be Constructive**: Provide actionable feedback with examples
2. **Prioritize**: Focus on critical issues first
3. **Explain Why**: Don't just point out problems, explain the reasoning
4. **Suggest Alternatives**: Offer concrete solutions or improvements
5. **Acknowledge Good Work**: Recognize well-written code and good practices
6. **Stay Objective**: Focus on the code, not the developer

## Example Reviews

### Example 1: Security Issue

**File**: `user_controller.py:45`

```python
# ❌ Problematic
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)
```

**Issue**: SQL injection vulnerability. User input is directly interpolated into SQL query.

**Suggested Fix**:
```python
# ✅ Better
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

### Example 2: Performance Issue

**File**: `data_processor.js:120`

```javascript
// ❌ Problematic
for (let item of items) {
  result += processItem(item);  // String concatenation in loop
}
```

**Issue**: Inefficient string concatenation in loop causes O(n²) performance.

**Suggested Fix**:
```javascript
// ✅ Better
const parts = items.map(item => processItem(item));
result = parts.join('');
```

## Guidelines for Reviewers

- Review code changes within 24 hours when possible
- Focus on objective improvements, not personal preferences
- Use inline comments for specific issues
- Provide summary comments for overall feedback
- Approve when code meets standards, even if minor improvements exist
- Request changes only for significant issues
- Use suggestions feature for minor fixes

## When to Use This Skill

Use this skill when:
- Reviewing pull requests
- Conducting code quality audits
- Onboarding new team members (teaching good practices)
- Refactoring legacy code
- Establishing coding standards
- Pre-release security reviews

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Clean Code Principles](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Google Style Guides](https://google.github.io/styleguide/)
- [Effective Code Review](https://google.github.io/eng-practices/review/)
