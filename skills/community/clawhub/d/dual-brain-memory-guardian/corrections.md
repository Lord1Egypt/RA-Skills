# Corrections Log - Template (Dual-Brain)

This file is created in `~/dual-brain-memory-guardian/corrections.md`.
Use it as a lightweight local audit and promotion tracker.
Detailed correction events live in Pinecone DEEP memory.

## Example Entries

```markdown
## 2026-04-04

### 14:32 - Code style
- Correction: "Use explicit return types"
- Context: TypeScript service refactor
- DEEP Event: default#correction#20260404T143200123#5f8c2a1b
- Promotion: pending (1/3)

### 16:15 - Auth flow
- Correction: "Refresh token requests must be single-flight"
- Context: Axios interceptor rewrite
- DEEP Event: default#correction#20260404T161500007#1a2b3c4d
- Promotion: promoted to projects/my-app.md
```

## Log Format

Each entry should include:

- Timestamp
- Correction summary
- Context
- Pinecone DEEP event id
- Promotion state (`pending`, `promoted`, `rejected`)

## Local Retention Guidance

- Keep this file compact and readable.
- Avoid storing full transcripts here.
- Use this file to track promotion decisions and references.
