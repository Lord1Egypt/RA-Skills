# Code Health Scanner — Design Draft

## Naming
- **Name:** code-health-scanner
- **Tagline:** "One-click Spring Boot code health diagnosis"
- **ClawHub id:** TBD

## Architecture: Single-Role Scanner
Unlike Writing Triadic (3-role), this uses a simpler model:
- **Scanner** (main AI): Read code files → detect issues → classify → report → offer auto-fix
- No sub-agents needed for most scans. Complex scans spawn a sub-agent per module.

## Detection Categories

### 🔴 Critical (Potential runtime failure)
1. SQL Injection: String concatenation in queries, no PreparedStatement
2. NPE Risk: Unchecked Optional.get(), null return without @Nullable
3. Resource Leak: Unclosed streams/connections in finally blocks
4. Hardcoded Secrets: API keys, passwords in source code
5. Transaction Missing: DB writes without @Transactional

### 🟡 Warning (Code smell, tech debt)
6. N+1 Query: Lazy loading in loops (JPA/Hibernate)
7. Exception Swallowing: Empty catch blocks, e.printStackTrace() in prod
8. God Class: >500 lines, >20 methods
9. Missing Index Hint: WHERE/ORDER BY columns without index comments
10. Deprecated API: @Deprecated usage without migration plan
11. Thread Safety: Shared mutable state in @Service/@Component
12. Missing Validation: @RequestBody without @Valid

### 🟢 Info (Style, convention)
13. Package Structure: Standard Spring Boot layout check
14. Naming Convention: camelCase, PascalCase violations
15. Comment Quality: TODO/FIXME count, missing Javadoc on public API
16. Dependency Health: pom.xml version freshness check (optional, needs Maven Central API)

## Scan Flow
```
1. Discover: Find all .java, .xml, .properties files
2. Filter: Skip test files (optional), skip generated code
3. Scan: Per-file issue detection
4. Aggregate: Merge findings, remove duplicates
5. Classify: Assign severity + category
6. Report: Generate markdown health report
7. Auto-fix: Offer fixes for low-risk issues (Critical/Warning need user review)
```

## Report Format
```markdown
# 🔍 Code Health Report

## Summary
- Scanned: 42 files, 8,500 LOC
- Critical: 2 | Warning: 7 | Info: 12
- Health Score: 72/100

## Critical Issues
### 1. SQL Injection in UserMapper.java:34
- Type: Security
- Fix: Replace string concatenation with #{param}

### 2. Hardcoded Secret in application.properties:15
- Type: Security
- Fix: Move to environment variable

## Warning Issues
...

## Info Issues
...
```

## Files Needed
1. SKILL.md — Main protocol
2. references/rules/java-spring.md — Detection rules catalog
3. references/report-template.md — Report format reference
4. CHANGELOG.md
5. README.md
6. LICENSE (MIT)

## Model Recommendation
- Default: deepseek-v4-flash (fast scanning, low cost)
- Complex analysis: deepseek-v4-pro
