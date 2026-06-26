---
name: code-review-expert
description: Multi-agent code review system using Manager-Worker pattern. Provides comprehensive code analysis from syntax, logic, security, and performance perspectives.
---

# Code Review Expert

AI-powered code review system that uses multiple specialized agents to analyze your code from different perspectives.

---

## Features

### 🔍 Multi-Dimensional Analysis

- **Syntax Checker**: ESLint standards, code formatting, naming conventions
- **Logic Reviewer**: Bug detection, edge cases, error handling
- **Security Scanner**: SQL injection, XSS, sensitive data exposure
- **Performance Analyzer**: Time complexity, optimization opportunities

### 📊 Detailed Reports

- Issue severity ratings (Critical/High/Medium/Low)
- Line-by-line feedback
- Concrete fix suggestions
- Code examples for improvements

### 🎯 Language Support

- JavaScript/TypeScript (primary)
- Python (basic)
- More languages coming soon

---

## Usage

### Basic Review

```javascript
const reviewer = new CodeReviewExpert();

const code = `
function getUser(userId) {
  const users = db.query('SELECT * FROM users');
  const user = users.find(u => u.id === userId);
  return user.name;
}
`;

const report = await reviewer.review(code);
console.log(report);
```

### Advanced Options

```javascript
const reviewer = new CodeReviewExpert({
  languages: ['javascript', 'typescript'],
  strictMode: true,  // More rigorous checks
  autoFix: false,    // Auto-generate fixes
  verbose: true
});

const report = await reviewer.review(code, {
  focus: ['security', 'performance'],  // Specific areas
  maxIssues: 10  // Limit issues
});
```

---

## Example Output

```markdown
## Code Review Report

### Overview
- File: user-service.js
- Issues Found: 5
- Critical: 1, High: 2, Medium: 1, Low: 1

### 🔴 Critical Issues

1. **SQL Injection Risk** (Line 2)
   ```javascript
   // Problem
   const query = `SELECT * FROM users WHERE id = ${userId}`;
   
   // Fix
   const query = 'SELECT * FROM users WHERE id = ?';
   db.execute(query, [userId]);
   ```

### 🟠 High Priority

2. **Null Pointer Risk** (Line 3)
   - `user` might be undefined
   - Add null check before accessing properties

### Overall Score: 6/10
```

---

## Architecture

```
Manager Agent (Coordinator)
    ↓
├─ Syntax Worker (ESLint rules)
├─ Logic Worker (Bug detection)
├─ Security Worker (Vulnerability scan)
└─ Performance Worker (Optimization)
    ↓
Report Aggregator → Final Report
```

---

## Installation

```bash
clawhub install code-review-expert
```

---

## API Reference

### `review(code, options)`

Review code and return report.

**Parameters**:
- `code` (string): Source code to review
- `options` (object): Review options
  - `focus`: Array of areas to focus on
  - `maxIssues`: Maximum issues to return
  - `includeSuggestions`: Include fix suggestions

**Returns**: Promise<ReviewReport>

### `ReviewReport`

```typescript
{
  score: number;           // 0-10
  issues: Issue[];
  summary: string;
  suggestions: string[];
}
```

---

## License

MIT

---

## Author

AI-Agent

---

## Version

1.0.0

---

## Created

2026-04-02
