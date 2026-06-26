#!/bin/bash
# Parallel Review Template Spawn Prompt
# Use for: Multi-lens code review (security + performance + tests)

cat << 'SPAWNPROMPT'
I need a comprehensive code review with 3 specialized perspectives: security, performance, and test coverage.

Target: ${TARGET_DIR}

Spawn 3 teammates using Sonnet (tactical reviews):

1. **Security Reviewer**
   - Name: security-reviewer
   - Focus: Authentication, authorization, input validation, SQL injection, XSS, CSRF, secrets management
   - Output: findings-security.md
   - Tasks:
     * Review authentication/authorization logic
     * Check input validation and sanitization
     * Identify potential injection vulnerabilities
     * Verify secrets are not hardcoded
     * Flag any security anti-patterns

2. **Performance Reviewer**
   - Name: performance-reviewer
   - Focus: Algorithmic complexity, database queries, caching, memory leaks, scaling issues
   - Output: findings-performance.md
   - Tasks:
     * Profile algorithmic complexity (O(n²) → O(n log n) opportunities)
     * Identify N+1 queries or missing indexes
     * Check for caching opportunities
     * Flag memory leak risks (unclosed connections, large objects in memory)
     * Assess scaling implications (will this work at 10x load?)

3. **Test Coverage Reviewer**
   - Name: test-reviewer
   - Focus: Test quality, coverage gaps, edge cases, flaky tests, integration vs unit balance
   - Output: findings-tests.md
   - Tasks:
     * Assess test coverage for changed code
     * Identify missing edge case tests
     * Check for flaky test patterns (timing, non-determinism)
     * Verify integration tests cover critical paths
     * Flag untestable code (suggest refactoring for testability)

Coordination rules:
- Use delegate mode: I coordinate, teammates review (I don't implement)
- Each reviewer works independently (no blocking dependencies)
- Reviewers should document findings with:
  * Severity (Critical / High / Medium / Low)
  * File + line number
  * Recommendation
  * Example fix (if applicable)
- Wait for all 3 reviewers to complete before I synthesize findings

After all teammates finish:
1. Read all 3 findings files
2. Synthesize into synthesis-review.md with:
   - Executive summary (top 3 issues)
   - Findings by severity (Critical first)
   - Recommendations prioritized by impact
3. Report completion with summary
SPAWNPROMPT
