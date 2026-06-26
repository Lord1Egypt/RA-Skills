---
name: code-analysis
description: Perform multi-dimensional advanced code analysis including knowledge graph generation, code quality evaluation, performance analysis, security review, architecture review, and test coverage analysis, outputting structured reports with actionable recommendations.
---

# Code Analysis

Perform multi-dimensional advanced code analysis, outputting structured reports and improvement roadmaps.

## Use Cases

Use when users need "code analysis", "code review", "code quality assessment", "performance analysis", or "security review".

## Analysis Dimensions

Select one or more based on user needs:

### 1. Knowledge Graph Generation
- Map relationships between components
- Visualize dependencies
- Identify architectural patterns

### 2. Code Quality Evaluation
- Complexity metrics (cyclomatic complexity, cognitive complexity)
- Maintainability index
- Technical debt assessment
- Code duplication detection

### 3. Performance Analysis
- Identify performance bottlenecks
- Memory usage patterns
- Algorithm complexity analysis
- Database query optimization recommendations

### 4. Security Review
- Vulnerability scanning
- Input validation checks
- Authentication/authorization review
- Sensitive data handling checks

### 5. Architecture Review
- Design pattern adherence
- SOLID principles compliance
- Coupling and cohesion analysis
- Module boundary assessment

### 6. Test Coverage Analysis
- Coverage percentages
- Untested code paths
- Test quality assessment
- Missing edge cases

## Workflow

1. Read user-provided code files or directories
2. Select analysis types based on user needs
3. Execute analysis and generate comprehensive report
4. Provide actionable improvement recommendations
5. Prioritize optimization items by impact

## Output Format

```
## Code Analysis Report

### Executive Summary
[Overall assessment overview, 1-2 paragraphs]

### Detailed Findings
#### [Dimension 1]
- Finding 1: xxx
- Finding 2: xxx

#### [Dimension 2]
- Finding 1: xxx

### Risk Assessment
| Risk Level | Issue | Impact Scope | Recommendation |
|------------|-------|--------------|----------------|
| 🔴 High | xxx | xxx | xxx |
| 🟡 Medium | xxx | xxx | xxx |
| 🟢 Low | xxx | xxx | xxx |

### Improvement Roadmap
1. Immediate fixes (high priority)
2. Short-term optimization (1-2 weeks)
3. Long-term improvements (1-3 months)

### Code Examples
[Code examples of key issues with improvement suggestions]
```