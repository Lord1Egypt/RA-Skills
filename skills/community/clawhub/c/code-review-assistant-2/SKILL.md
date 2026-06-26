---
name: code-review-assistant
description: AI-powered code review assistant that analyzes pull requests, identifies potential bugs, security issues, code quality problems, and provides actionable improvement suggestions. Use when reviewing PRs, auditing code changes, or ensuring code quality standards.
version: 1.0.0
author: muqing
tags: [development, code-review, security, quality]
---

# Code Review Assistant

## Description

An AI-powered code review assistant that analyzes pull requests, identifies potential bugs, security vulnerabilities, code quality issues, and provides actionable improvement suggestions. This skill helps maintain code quality standards and catch issues before they reach production.

## When to Use

- Reviewing pull requests for potential issues
- Auditing code changes for security vulnerabilities
- Ensuring code follows best practices and style guides
- Identifying performance bottlenecks
- Checking for test coverage gaps
- Validating code complexity

## Review Checklist

### Security Issues
- SQL injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Authentication/authorization flaws
- Sensitive data exposure
- Insecure dependencies

### Code Quality
- Code duplication
- Function/class complexity
- Naming conventions
- Comment quality
- Error handling
- Resource management

### Performance
- N+1 query problems
- Unnecessary re-renders
- Memory leaks
- Inefficient algorithms
- Missing caching opportunities

### Best Practices
- Test coverage
- Documentation completeness
- API consistency
- Error handling patterns
- Type safety

## How to Use

1. When asked to review code, first gather context:
   - The programming language and framework
   - The files/functions changed
   - The purpose of the changes

2. Analyze the code systematically using the checklist

3. Provide structured feedback with severity levels

## Output Format

```
## Code Review Summary

### Overview
[Brief description of what the PR does]

### Issues Found

#### Critical (🔴)
- [Issue with location and fix suggestion]

#### High (🟠)
- [Issue with location and fix suggestion]

#### Medium (🟡)
- [Issue with location and fix suggestion]

#### Low (🟢)
- [Minor suggestions]

### Positive Aspects
- [What was done well]

### Recommendations
- [Additional suggestions]
```
