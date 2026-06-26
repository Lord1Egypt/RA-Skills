---
name: code-review-checklist
description: 代码审查清单 - A comprehensive code review checklist and guidance tool. Use when user asks about 代码审查、代码检查、PR review、代码质量, or wants to conduct or prepare for a code review. Provides systematic checklist items and best practices.
---

# Code Review Checklist (代码审查清单)

## Overview

This skill provides a systematic approach to code reviews. It offers comprehensive checklist items across multiple dimensions of code quality, helps reviewers focus on high-impact areas, and guides developers in preparing code for review. Designed to make code reviews more efficient and thorough.

## When to Use This Skill

- Preparing code for pull request review
- Conducting a code review as a reviewer
- Self-reviewing own code before submission
- Establishing code review standards for a team
- Training new developers on review best practices
- Auditing code quality in a codebase

## What This Skill Provides

### 1. Predefined Checklists
Comprehensive checklist items organized by category:
- Code correctness and logic
- Code style and readability
- Performance and efficiency
- Security considerations
- Error handling
- Testing coverage
- Documentation
- Architecture and design patterns

### 2. Review Guidance
- What to look for in each category
- Red flags and common issues
- Best practices specific to language/framework
- Questions to ask the author

### 3. Review Workflow
- Systematic approach to reviewing
- Priority ordering of checks
- Time allocation guidance
- Documentation requirements

## Checklist Categories

### 1. Correctness & Logic
- [ ] Code produces expected output
- [ ] Edge cases are handled
- [ ] No off-by-one errors
- [ ] Logic is sound and complete
- [ ] No infinite loops or recursion issues
- [ ] Proper use of data structures

### 2. Code Style & Readability
- [ ] Follows project coding standards
- [ ] Naming is clear and descriptive
- [ ] Functions are appropriately sized
- [ ] Code is not duplicated (DRY principle)
- [ ] Complex logic has comments
- [ ] Formatting is consistent

### 3. Performance & Efficiency
- [ ] No unnecessary loops or iterations
- [ ] Proper use of caching when applicable
- [ ] Database queries are optimized
- [ ] No memory leaks
- [ ] Appropriate algorithmic complexity
- [ ] Resources are properly released

### 4. Security
- [ ] Input validation on all user inputs
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Secrets not hardcoded
- [ ] Proper authentication/authorization
- [ ] Sensitive data properly protected
- [ ] No security misconfigurations

### 5. Error Handling
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are user-friendly
- [ ] No empty catch blocks
- [ ] Logging is appropriate
- [ ] Graceful degradation where needed
- [ ] No exposing internal error details

### 6. Testing
- [ ] Unit tests exist for new code
- [ ] Tests cover happy path and edge cases
- [ ] Tests are maintainable
- [ ] Mock usage is appropriate
- [ ] Test coverage meets requirements
- [ ] No flaky tests introduced

### 7. Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] API changes are documented
- [ ] Breaking changes are noted

### 8. Architecture & Design
- [ ] Follows project architecture patterns
- [ ] Single Responsibility Principle followed
- [ ] Dependencies are properly injected
- [ ] Coupling is minimized
- [ ] Changes are localized appropriately
- [ ] No tech debt introduced unnecessarily

## Language-Specific Considerations

### JavaScript/TypeScript
- Proper async/await usage
- TypeScript types are correct
- No 'any' type abuse
- ESLint rules followed

### Python
- PEP 8 compliance
- Type hints where appropriate
- Docstrings for public functions
- No deprecated imports

### Java
- Null safety considerations
- Resource management (try-with-resources)
- Stream API usage
- Concurrent access considerations

### Go
- Error handling conventions
- Goroutine leak prevention
- Context usage
- Naming conventions

## Review Workflow

### Step 1: Context (2-3 min)
- Read PR description and motivation
- Understand what changed and why
- Check related issues or docs

### Step 2: Overview (3-5 min)
- Scan changed files
- Identify high-risk areas
- Note files needing deep review

### Step 3: Detailed Review (15-30 min)
- Follow checklist by priority
- Comment on issues found
- Ask clarifying questions
- Suggest improvements

### Step 4: Summary (3-5 min)
- Summarize findings
- Categorize issues (Blocking/Suggestion/Question)
- Approve or request changes

## Usage Examples

### As a Reviewer
```
"用代码审查清单检查这个PR"
"帮我审查这个函数的逻辑"
"检查这段代码有没有安全问题"
"看看这个文件有哪些可以改进的地方"
```

### As a Developer
```
"帮我准备代码审查"
"自审查这份代码,有什么遗漏?"
"检查这段代码的测试覆盖"
"这个代码符合项目规范吗?"
```

### For Team Standards
```
"生成一个代码审查检查清单"
"我们团队的代码审查标准是什么?"
"前端代码审查有什么特殊要求?"
```

## Output Format

For each review, output:

```markdown
## Code Review: [PR/Change Title]

### Summary
- Files changed: X
- Lines added/removed: +X/-X
- Risk level: [Low/Medium/High]

### Findings

#### 🔴 Blocking Issues
- [Issue description] - [File:Line] - [Suggestion]

#### 🟡 Suggestions
- [Suggestion] - [File:Line]

#### 🟢 Good Practices Noted
- [Positive observation]

### Checklist Status
- [x] Correctness
- [x] Style
- [ ] Security (needs work)
- [x] Performance

### Recommendation
[Approve / Request Changes / Discuss]

### Action Items
- [ ] Item 1
- [ ] Item 2
```

## Integration with Development Workflow

This skill integrates with:
- `github` — For reviewing PRs directly
- `coding-agent` — For automated code quality checks
- `opencli` — For running linters and formatters

## Limitations

- Cannot execute code to verify correctness
- Cannot know full system context
- Best practices may vary by project
- Language-specific items may be incomplete for niche languages

## Acceptance Criteria

1. ✓ Provides comprehensive checklist coverage
2. ✓ Can customize for different languages/frameworks
3. ✓ Identifies common issues efficiently
4. ✓ Helps categorize issue severity
5. ✓ Provides actionable feedback
6. ✓ Saves time in review process
7. ✓ Helps developers learn and improve
