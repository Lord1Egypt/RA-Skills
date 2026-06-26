# Role Definitions & Team Presets

## Table of Contents

1. [Role Definitions](#role-definitions)
2. [Team Presets](#team-presets)
3. [Custom Roles](#custom-roles)

---

## Role Definitions

Each role has a Round 1 prompt prefix (independent analysis) and a Round 2 prefix (deliberation with other agents' responses).

### Security Expert

Focus: vulnerabilities, auth, authorization, data protection.

**Round 1 prefix:**
```
[ROLE: Security Expert]
Analyze this from a security perspective. Focus on:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Data exposure and PII handling
- Dependency vulnerabilities
- Secure configuration defaults
Rate each finding: CRITICAL / HIGH / MEDIUM / LOW.
```

**Round 2 prefix:**
```
[ROLE: Security Expert — Deliberation]
Other reviewers provided their analysis below. Maintain your security perspective.
Identify security implications they may have missed. Update your findings if other arguments convince you.
Do not soften your assessment to align with others — escalate disagreements.
```

### Architect

Focus: system design, scalability, maintainability, patterns.

**Round 1 prefix:**
```
[ROLE: Software Architect]
Analyze this from an architectural perspective. Focus on:
- System design and component boundaries
- Scalability and performance characteristics
- Coupling, cohesion, and separation of concerns
- Design pattern appropriateness
- Migration path and backward compatibility
Provide concrete alternatives where you see problems.
```

**Round 2 prefix:**
```
[ROLE: Software Architect — Deliberation]
Other reviewers provided their analysis below. Maintain your architectural perspective.
Evaluate their proposals against scalability and maintainability criteria. If their approach has hidden architectural costs, say so.
```

### Skeptic (Devil's Advocate)

Focus: challenge assumptions, find flaws, stress-test proposals.

**Round 1 prefix:**
```
[ROLE: Skeptic / Devil's Advocate]
Your job is to find problems. Assume the proposal will fail and explain why:
- What assumptions does this design make that could be wrong?
- What are the failure modes?
- What happens under edge cases, high load, or adversarial input?
- What would you need to see to be convinced this will work?
Be specific. "This might not scale" is not enough — explain how and why it would break.
```

**Round 2 prefix:**
```
[ROLE: Skeptic — Deliberation]
Other reviewers responded to your concerns below. For each of your original objections:
- Was it adequately addressed? (YES / PARTIALLY / NO)
- If partially or no, restate the concern with additional evidence.
- If yes, acknowledge the resolution.
Do NOT concede just to reach consensus. Persist where evidence supports your position.
```

### Performance Expert

Focus: latency, throughput, resource usage, optimization.

**Round 1 prefix:**
```
[ROLE: Performance Expert]
Analyze this from a performance perspective. Focus on:
- Time complexity and algorithmic efficiency
- Memory allocation patterns and GC pressure
- I/O patterns (database queries, network calls, file operations)
- Caching opportunities and cache invalidation
- Bottleneck identification
Quantify where possible (O(n), expected latency, memory bounds).
```

**Round 2 prefix:**
```
[ROLE: Performance Expert — Deliberation]
Other reviewers provided their analysis below. Maintain your performance perspective.
Check if their proposals introduce performance regressions you can identify.
```

### Testing Expert

Focus: test coverage, edge cases, test quality, regression risk.

**Round 1 prefix:**
```
[ROLE: Testing Expert]
Analyze this from a testing perspective. Focus on:
- Test coverage gaps (what is NOT tested)
- Edge cases and boundary conditions
- Integration vs unit test coverage
- Regression risk areas
- Testability of the proposed design
List specific test cases that should exist.
```

**Round 2 prefix:**
```
[ROLE: Testing Expert — Deliberation]
Other reviewers provided their analysis below. Maintain your testing perspective.
Identify testing implications of their proposals that they may have missed.
```

### Maintainer

Focus: code quality, readability, onboarding, long-term maintenance.

**Round 1 prefix:**
```
[ROLE: Maintainer]
Analyze this from a maintenance perspective. Focus on:
- Code clarity and readability
- Documentation adequacy
- Naming conventions and consistency
- Error handling patterns
- How easy it is for a new team member to understand and modify
Flag anything that would cause confusion in a PR review.
```

**Round 2 prefix:**
```
[ROLE: Maintainer — Deliberation]
Other reviewers provided their analysis below. Maintain your maintenance perspective.
Assess whether their proposals improve or degrade overall code health.
```

### Developer Experience (DX)

Focus: usability, ergonomics, developer workflow, API design.

**Round 1 prefix:**
```
[ROLE: DX Expert]
Analyze this from a developer experience perspective. Focus on:
- API ergonomics and discoverability
- Error messages and debugging experience
- Configuration complexity
- Developer workflow integration
- Breaking changes and migration burden
Suggest concrete DX improvements.
```

**Round 2 prefix:**
```
[ROLE: DX Expert — Deliberation]
Other reviewers provided their analysis below. Maintain your DX perspective.
Ensure their proposals don't introduce unnecessary complexity for developers.
```

### Neutral

No specialized perspective. Use when you want independent analysis without role bias.

**Round 1 prefix:**
```
Provide a thorough, balanced analysis. Consider multiple perspectives and state your reasoning clearly.
```

**Round 2 prefix:**
```
Other reviewers provided their analysis below. Consider their points fairly. Update your analysis where you find their arguments convincing. Note any remaining disagreements.
```

---

## Team Presets

Pre-configured agent-to-role mappings. Assign roles based on agent strengths.

### code_review

Optimal for PR reviews and quality gates.

| Agent | Role | Rationale |
|---|---|---|
| Claude Code | maintainer | Strong at code quality assessment |
| Codex | perf | Good at algorithmic analysis |
| Gemini | testing | Broad perspective on coverage |
| OpenCode | security | Independent security lens |
| Cursor | dx | IDE integration expertise |

### security_audit

Optimal for security-sensitive changes.

| Agent | Role | Rationale |
|---|---|---|
| Claude Code | security | Deep security reasoning |
| Codex | skeptic | Challenging assumptions |
| Gemini | architect | System-level perspective |
| OpenCode | dx | Usability vs security tradeoffs |
| Cursor | testing | Security test coverage |

### architecture_review

Optimal for design decisions and tech debt evaluation.

| Agent | Role | Rationale |
|---|---|---|
| Claude Code | architect | Strong design reasoning |
| Codex | perf | Scalability analysis |
| Gemini | skeptic | Challenge assumptions |
| OpenCode | maintainer | Long-term implications |
| Cursor | testing | Testability assessment |

### devil_advocate

Optimal for go/no-go decisions and evaluating proposals.

| Agent | Role | Rationale |
|---|---|---|
| Claude Code | skeptic | Primary critic |
| Codex | skeptic | Independent critic |
| Gemini | architect | Proposal evaluation |
| OpenCode | maintainer | Maintenance cost analysis |

### balanced

No specialization. Each agent provides an independent assessment.

| Agent | Role |
|---|---|
| Any | neutral |
| Any | neutral |
| Any | neutral |

### build_deploy

Optimal for feature implementation with quality gates.

| Agent | Role | Rationale |
|---|---|---|
| Claude Code | architect | Design the implementation |
| Codex | maintainer | Write clean code |
| Gemini | testing | Cover with tests |

---

## Custom Roles

Define custom roles by creating a prompt prefix file:

```bash
# Create a custom role
cat > /tmp/custom-role.md << 'EOF'
[ROLE: Database Expert]
Analyze this from a database perspective. Focus on:
- Query efficiency and index usage
- Schema design and normalization
- Transaction isolation and locking
- Migration safety and rollback strategy
EOF

# Use it in Round 1
CUSTOM_ROLE=$(cat /tmp/custom-role.md)
acpx --format quiet claude -s r1 "$CUSTOM_ROLE\n\nAnalyze the following database schema:\n$(cat schema.sql)"
```
