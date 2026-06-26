# RFC Template

This template provides the standard structure for writing RFCs (Request for Comments) for open-source projects. Follow this structure when writing RFCs in Phase 5.

---

```markdown
# RFC: [Concise Title]

## Metadata

| Field | Value |
|-------|-------|
| **Author** | [Your name / handle] |
| **Date** | [YYYY-MM-DD] |
| **Status** | Draft |
| **Target Repository** | [owner/repo] |
| **Related Issues** | #[issue numbers] |

## Problem Statement

[Describe the problem in 2-3 paragraphs. Include:]

- What is broken, missing, or suboptimal?
- Who is affected and how?
- Quantify the impact with metrics (e.g., "40% of API endpoints lack input validation")
- Reference specific code locations: `path/to/file.ts:42-58`

**Evidence:**

| Metric | Value | Source |
|--------|-------|--------|
| [Metric name] | [Number/Percentage] | [Code location or issue] |

## Prior Art

### Academic Research

- **[Author et al., Year]**: "[Paper Title]" — [1-sentence summary of relevance]
- **[Author et al., Year]**: "[Paper Title]" — [1-sentence summary of relevance]

### Existing Solutions

- **[Project/Tool]**: [How it solves or relates to this problem]
- **[Project/Tool]**: [How it solves or relates to this problem]

### Community Context

- Issue #[N]: [Summary of community discussion]
- Discussion #[N]: [Summary of maintainer feedback]

## Proposed Solution

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Layer 4: Governance             │
│  (policy enforcement, audit, monitoring)     │
├─────────────────────────────────────────────┤
│             Layer 3: Intelligence            │
│  (ML models, pattern recognition, insights)  │
├─────────────────────────────────────────────┤
│             Layer 2: Enhancement             │
│  (core features, APIs, integrations)         │
├─────────────────────────────────────────────┤
│              Layer 1: Foundation             │
│  (data models, storage, collection)          │
└─────────────────────────────────────────────┘
```

### Data Models

```typescript
// Example data model definition
interface [ModelName] {
  id: string;
  // ... fields
}
```

### API Design

```
POST /api/v1/[resource]      — Create [resource]
GET  /api/v1/[resource]/:id  — Read [resource]
PUT  /api/v1/[resource]/:id  — Update [resource]
```

### Implementation Phases

| Phase | Scope | Timeline | Deliverables |
|-------|-------|----------|-------------|
| Phase 1 | Foundation | Weeks 1-4 | [Deliverables] |
| Phase 2 | Enhancement | Weeks 5-8 | [Deliverables] |
| Phase 3 | Intelligence | Weeks 9-12 | [Deliverables] |
| Phase 4 | Governance | Weeks 13-16 | [Deliverables] |

## Trade-offs

### Benefits

- [Benefit 1 with quantified impact]
- [Benefit 2 with quantified impact]

### Costs

- [Cost 1: performance, complexity, migration effort]
- [Cost 2: ...]

### Migration Path

1. [Step 1: backward-compatible introduction]
2. [Step 2: deprecation warnings]
3. [Step 3: removal of old behavior]

### Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk] | Low/Med/High | Low/Med/High | [Mitigation strategy] |

## Open Questions

- [ ] [Question 1 needing community input]
- [ ] [Question 2 needing community input]

## Call for Collaboration

We're looking for help with:

- [ ] [Specific task 1] — [Required skills]
- [ ] [Specific task 2] — [Required skills]

To get involved:
1. Comment on this issue with your interest
2. Review the proposed architecture and share feedback
3. Pick an open question to investigate

## References

1. [Author et al., Year]. "[Title]" [Conference/Journal]. [URL]
2. [Source]. [URL]
3. GitHub Issue #[N]: [URL]
```

---

## Writing Tips

1. **Be specific**: Replace all `[placeholders]` with actual content. No placeholders should remain in the final RFC.
2. **Quantify everything**: Use numbers, percentages, and measurements instead of vague terms like "many" or "slow".
3. **One RFC per topic**: Keep the scope focused. Split into multiple RFCs if needed.
4. **ASCII diagrams**: Use simple ASCII art for architecture diagrams — they render in any markdown viewer.
5. **Link, don't inline**: Reference issues and discussions by number/URL rather than copying their content.
