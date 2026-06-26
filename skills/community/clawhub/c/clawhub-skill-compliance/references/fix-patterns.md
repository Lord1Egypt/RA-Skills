# Fix Patterns

> Quick fix patterns for skill compliance

---

## 1. Metadata

```yaml
---
name: skill-name
description: "What it does. Use when: X, Y. NOT for: simple Z."
dependencies:
  skills: [name]
  tools: [bash, read]
env:
  optional: [API_KEY]
---
```

---

## 2. Dependencies

**Declare all references:**
- External skill → `dependencies.skills`
- Tools used → `dependencies.tools`
- Make loading optional

**Principle**: Be transparent about all dependencies.

---

## 3. Environment Variables

```yaml
env:
  optional:
    - SUPABASE_URL
    - SUPABASE_ANON_KEY
```

**Placeholder format**: Use `<your-key>` with annotation.

---

## 4. Security Scope

```markdown
## Security Scope
**What this skill does**: [list]
**What this skill does NOT**: [list]
```

Keep security information visible for reviewers.

---

## 5. Consistency

- Header says NOT X → Examples should not show X
- Be precise in descriptions

---

## 6. Platform Commands

Mark as optional:
```markdown
Note: `command` is optional for PlatformX.
```

---

## 7. Content Clarity

**Simplification guidelines:**
- Use tables for command lists
- Keep examples concise
- Use annotated placeholders

**Annotated placeholder examples:**
- `<your-api-key>` - API key placeholder
- `<project-url>` - Project URL placeholder
- `<binary-name>` - Installed binary name

**Keep**: Security scope, dependencies, purpose.

---

## 8. Safe Package References

**Recommended**: Global install
```bash
npm install -g <package>
"command": ["<binary-name>"]
```

**Avoid**: `npx -y` (bypasses verification)

**Principle**: Verify packages before use.

---

## Transparency Checklist

Before publishing, verify:
- [ ] All dependencies declared
- [ ] All env vars declared
- [ ] Security scope present
- [ ] No hardcoded secrets
- [ ] Placeholders are annotated
- [ ] Content is clear and accurate

---

*Fix Patterns v2.2 - 2026-04-05*