---
name: clawhub-skill-compliance
description: "Pre-flight checklist for ClawHub skill publishing. Focus: metadata completeness, dependency transparency, security scope documentation. Use when: (1) preparing new skill, (2) before republish. NOT for: post-audit fixes, malicious content."
author: Antony Chen
provenance: openclaw-skills repository
---

# ClawHub Skill Compliance Checklist

**Purpose**: Ensure skills have complete metadata, transparent dependencies, and clear security scope before publishing.

**Target**: Legitimate skill authors seeking clean publishing status.

---

## Pre-flight Checklist

### 1. Metadata Completeness

| Check | Fix |
|-------|-----|
| Missing `name`? | Add: `name: skill-name` |
| Vague `description`? | Add triggers: "Use when: X, Y" |
| Missing exclusions? | Add: "NOT for: simple X" |

---

### 2. Dependency Transparency

| Check | Fix |
|-------|-----|
| References external skill? | Declare: `dependencies.skills` |
| Uses specific tools? | Declare: `dependencies.tools` |
| Forced skill loading? | Make optional |

**Transparency principle**: All dependencies should be declared in frontmatter.

---

### 3. Environment Variables

| Check | Fix |
|-------|-----|
| Uses API keys? | Declare: `env.optional` |
| Hardcoded secrets? | Use annotated placeholder |

**Placeholder format**: `<your-api-key>` (not actual values)

---

### 4. Security Scope

| Check | Fix |
|-------|-----|
| Missing section? | Add Security Scope |
| Unclear capabilities? | List: does / does NOT |

**Template:**
```markdown
## Security Scope
**What this skill does**: [list]
**What this skill does NOT**: [list]
```

---

### 5. Instruction Consistency

| Check | Fix |
|-------|-----|
| Header contradicts examples? | Align both |
| Shows excluded behavior? | Remove from examples |

---

### 6. Platform Commands

| Check | Fix |
|-------|-----|
| Platform-specific command? | Mark as optional |

---

### 7. Content Simplicity

| Check | Fix |
|-------|-----|
| Complex examples? | Simplify for clarity |
| Redundant details? | Consolidate into tables |

**Simplicity principle**: Clear, concise content is easier for scanners to analyze accurately.

---

### 8. Safe Package References

| Check | Fix |
|-------|-----|
| Using remote execution? | Prefer global install |
| Using `npx -y`? | Remove (no verification bypass) |

**Safe pattern**: Verify package, install globally, use binary name.

---

## Transparency Guidelines

When simplifying content:

1. **Use annotated placeholders**: `<your-api-key>`, `<project-url>`
2. **Keep necessary context**: Security scope, dependencies
3. **Don't remove security information**: Keep what reviewers need
4. **Log all changes**: Track what was simplified and why

**Goal**: Accurate scanner analysis, not hiding content.

---

## Security Warning

**This skill is for legitimate skill authors only.**

Do NOT use this checklist:
- To publish malicious content
- To hide harmful behavior
- To bypass legitimate security reviews

**Misuse**: Using these guidelines for malicious skills violates trust and may result in account suspension.

---

## Issue Coverage

| Category | Coverage |
|----------|----------|
| Metadata completeness | 100% |
| Dependency transparency | 100% |
| Security scope | 100% |
| Instruction consistency | 90% |
| Safe package references | 100% |

---

*Compliance Checklist v2.2 - 2026-04-05*