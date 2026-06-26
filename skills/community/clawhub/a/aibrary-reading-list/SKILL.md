---
name: aibrary-reading-list
description: "[Aibrary] Generate a curated, themed reading list with multiple books organized in a logical reading order. Use when the user wants a systematic book list on a topic, asks for a book list or reading list, wants to deeply explore a domain through multiple books, or needs to build expertise in an area. Different from aibrary-book-recommend (single book) and aibrary-book-search (finding specific books)."
---

# Reading List — Aibrary

Curated, themed reading lists that build expertise systematically. Powered by Aibrary's knowledge curation methodology.

## Input

The user specifies:
- **Theme/domain** — the area they want to explore (required)
- **Difficulty preference** — beginner, intermediate, advanced, or mixed (optional, default: mixed)
- **Number of books** — how many they want (optional, default: 7-10)
- **Constraints** — time period, language, specific focus within the domain (optional)

## Workflow

1. **Define the scope**: Clarify what the theme covers and what's out of scope. If the theme is too broad, suggest 2-3 focused sub-themes for the user to choose from.

2. **Select books**: Choose books that collectively cover the theme comprehensively:
   - Include foundational works that establish core concepts
   - Include modern works that reflect current thinking
   - Include contrasting perspectives to encourage critical thinking
   - Ensure no significant aspect of the theme is left uncovered

3. **Organize the reading order**: Arrange books in a logical progression:
   - **Foundation first**: Conceptual and introductory works
   - **Build depth**: More specialized and advanced works
   - **Synthesize**: Works that connect ideas across the theme
   - Mark books as "Essential" (must-read) or "Recommended" (nice to have)

4. **Add connective tissue**: Explain how each book connects to the next and what the reader gains at each stage.

5. **Respond in the user's language**: Match the language of the user's input.

## Output Format

```
# Reading List: [Theme Name]

[1-2 sentence overview of what this reading list covers and who it's for]

**Total books**: [Count] | **Estimated total reading time**: [Hours] | **Difficulty**: [Level range]

---

## Stage 1: Foundation
*[What the reader gains from this stage]*

### 1. [Book Title] ⭐ Essential
**Author**: [Name] | **Year**: [Year]
[One sentence on what this book contributes to the theme]

### 2. [Book Title]
**Author**: [Name] | **Year**: [Year]
[One sentence on what this book contributes to the theme]

**Stage 1 → Stage 2 bridge**: [How the foundation prepares the reader for deeper exploration]

---

## Stage 2: Depth
*[What the reader gains from this stage]*

### 3. [Book Title] ⭐ Essential
...

---

## Stage 3: Synthesis
*[What the reader gains from this stage]*

...

---

## Quick-Start Option
*If you only have time for 3 books, read these*:
1. [Book] — [Why]
2. [Book] — [Why]
3. [Book] — [Why]
```

### Example Output

**User input**: "Give me a reading list about systems thinking"

---

# Reading List: Systems Thinking

A progressive journey from understanding systems basics to applying systems thinking in complex real-world scenarios. Ideal for leaders, engineers, and anyone who wants to see the bigger picture.

**Total books**: 8 | **Estimated total reading time**: ~50 hours | **Difficulty**: Beginner → Advanced

---

## Stage 1: Foundation
*Build your mental models for understanding systems*

### 1. Thinking in Systems ⭐ Essential
**Author**: Donella Meadows | **Year**: 2008
The definitive introduction to systems thinking — clear, accessible, and surprisingly practical for a book about feedback loops.

### 2. The Fifth Discipline
**Author**: Peter Senge | **Year**: 2006 (revised)
Bridges systems thinking into organizational learning — essential for applying systems ideas in team and business contexts.

**Stage 1 → Stage 2 bridge**: With the fundamentals in place, you're ready to see how systems thinking applies to specific domains and complex challenges.

---

## Quick-Start Option
*If you only have time for 3 books, read these*:
1. **Thinking in Systems** — The essential foundation
2. **The Fifth Discipline** — Systems thinking in practice
3. **Seeing the Forest for the Trees** — Visual systems mapping

---

## Guidelines

- A reading list tells a story — books should build on each other, not just be a collection
- Always include a "Quick-Start Option" for time-constrained readers
- Mark essential vs. recommended books clearly
- Include bridge explanations between stages
- Balance classics with modern works
- If the theme is too broad, proactively narrow it or offer sub-theme options
