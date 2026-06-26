# Memory Integration Guide

## Overview

This guide explains how to integrate document learning progress with OpenClaw's memory system (MEMORY.md and daily notes).

## Learning Workflow

### 1. Initial Document Import

When starting to learn a new document:

```markdown
## 📚 Document Learning Progress

**Document:** [filename.pdf]  
**Started:** YYYY-MM-DD  
**Status:** In Progress / Completed  

### Summary
[Brief description of what this document is about]

### Key Concepts Learned
- Concept 1
- Concept 2
- ...
```

### 2. Progressive Learning Notes

During learning sessions, add entries to `memory/YYYY-MM-DD.md`:

```markdown
### Document Learning Session - [Date]

**Progress:** Chapter X of Y (XX% complete)

#### What I Learned Today
- Main point 1
- Main point 2  
- Important insight: [...]

#### Questions for Later
- Question about concept X
- Need to verify Y

#### Action Items
- Follow up on Z
- Apply concept A to project B
```

### 3. Final Integration

After completing the document, create a comprehensive summary in MEMORY.md:

```markdown
## Document Knowledge Base

### [Document Title] ([Date])

**Source:** `[filename.pdf]`  
**Duration:** X hours over Y days  

#### Complete Summary
[Comprehensive overview of all key concepts]

#### Detailed Notes
- **Topic 1**: Explanation and examples
- **Topic 2**: Important details and edge cases
- **Topic 3**: Practical applications

#### References
- Related documents: [link to other docs]
- External resources: [useful links]
```

## Progress Tracking Patterns

### Pattern 1: Chapter-based Learning

For structured documents (books, manuals):

```
Progress Tracker for [Document]:
- ✅ Chapter 1: Introduction
- ✅ Chapter 2: Core Concepts  
- 🔄 Chapter 3: Advanced Topics (60% complete)
- ⏳ Chapter 4: Implementation
- ⏳ Chapter 5: Best Practices
```

### Pattern 2: Page-based Learning

For reference materials and PDFs:

```
Page Progress: XX/XXX pages read

Last Session:
- Read pages X-X on YYYY-MM-DD
- Key takeaway: [summary]
- Next up: pages X+1 onwards
```

## Memory Search Integration

Once knowledge is stored in memory files, you can use OpenClaw's `memory_search` tool to find relevant information later.

### Example Queries

- "What did I learn about [topic] from [document]?"
- "Show me all notes about [concept]"
- "Summarize my learning progress on [subject]"

## Best Practices

1. **Consistency**: Add learning notes after each session, even if brief
2. **Specificity**: Include page numbers or chapter references for easy lookup
3. **Reflection**: Note questions and insights, not just facts
4. **Connection**: Link new knowledge to existing concepts in memory
5. **Review**: Periodically review past sessions to reinforce learning

## Automation Tips

You can automate progress tracking by:

1. Using the `read_large_document.py` script to extract text and key points
2. Automatically creating progress entries in daily notes
3. Generating summaries for MEMORY.md integration

See `scripts/read_large_document.py` for implementation details.
