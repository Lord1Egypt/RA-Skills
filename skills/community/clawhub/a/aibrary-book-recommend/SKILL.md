---
name: aibrary-book-recommend
description: "[Aibrary] Recommend books based on user interests, goals, challenges, or career stage. Use when the user asks for book recommendations, says they don't know what to read, wants personalized suggestions, or needs guidance on which book to pick next. Different from aibrary-book-search — this focuses on personalized recommendations rather than search results."
---

# Book Recommend — Aibrary

Personalized book recommendations tailored to who you are and where you're headed. Powered by Aibrary's recommendation methodology.

## Input

The user provides context about themselves:
- **Interest area** — what topics fascinate them
- **Current challenge** — what problem they're facing right now
- **Career stage** — student, early career, mid-career, senior, transitioning
- **Recent reads** — books they've enjoyed or found useful (optional)
- **Preference** — practical vs. theoretical, short vs. deep, etc. (optional)

## Workflow

1. **Build a reader profile**: From the user's input, identify:
   - Knowledge level in the relevant domain(s)
   - Whether they need foundational knowledge or advanced insights
   - Their learning style preference (if mentioned)
   - Time/effort they're willing to invest

2. **Select recommendations**: Choose 1-3 books (focused, not overwhelming). For each, ensure:
   - It fills a genuine knowledge gap for this specific person
   - It matches their current stage and challenge
   - It builds on what they already know (if prior reading is mentioned)

3. **Provide deep rationale**: Go beyond "this is a great book" — explain the specific connection between the book and the user's situation.

4. **Suggest a reading approach**: For each book, suggest how to get the most value (read cover-to-cover, focus on specific chapters, combine with practice, etc.)

5. **Respond in the user's language**: Match the language of the user's input.

## Output Format

```
## Your Recommendation

Based on [brief summary of user context], here's what I recommend:

### [Book Title]
**Author**: [Author Name]
**Published**: [Year] | **Pages**: [Count] | **Reading time**: [Estimate]

**Why this is right for you**: [2-3 sentences connecting the book specifically to the user's situation, goals, and current knowledge level]

**What you'll gain**:
- [Key takeaway 1]
- [Key takeaway 2]
- [Key takeaway 3]

**How to read it**: [Specific reading strategy — which parts to focus on, what to skip, how to apply the ideas]

**After this, read**: [One follow-up book suggestion to continue the learning path]
```

### Example Output

**User input**: "I'm a senior engineer thinking about whether to go into management. I've been reading a lot of technical books but nothing about leadership."

---

## Your Recommendation

Based on your transition consideration from senior engineer to management, with a strong technical background but limited leadership reading, here's what I recommend:

### The Manager's Path
**Author**: Camille Fournier
**Published**: 2017 | **Pages**: 244 | **Reading time**: ~6 hours

**Why this is right for you**: Written by a former CTO who started as an engineer, this book maps the exact journey you're considering. Unlike generic leadership books, it speaks your language and addresses the specific challenges engineers face when moving into management — from the first awkward 1:1 to managing managers.

**What you'll gain**:
- A realistic preview of what management actually looks like at each level
- Frameworks for deciding if management is right for you (it's not for everyone, and that's okay)
- Practical skills for the first 90 days as a new manager

**How to read it**: Start with chapters 1-4 to understand the progression from tech lead to manager. If you're still interested after chapter 3, the role is likely a good fit. Chapter 5 onwards is for when you've made the decision.

**After this, read**: *An Elegant Puzzle* by Will Larson — for the systems-thinking approach to engineering management.

---

## Guidelines

- Fewer, better recommendations beat a long list — 1-3 books maximum
- Always explain why this book, for this person, at this time
- Include practical reading strategies, not just "read this"
- Suggest what to read next to create a learning path
- If the user's needs are unclear, ask 1-2 clarifying questions first
- Distinguish from `aibrary-book-search`: search is for finding books on a topic; recommend is for personalized guidance on what to read next
