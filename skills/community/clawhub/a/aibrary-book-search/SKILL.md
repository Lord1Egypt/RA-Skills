---
name: aibrary-book-search
description: "[Aibrary] Search and find books based on user scenarios, needs, questions, or keywords. Use when the user describes a situation, challenge, or topic and wants to find relevant books to read. Trigger on phrases like 'find me a book about', 'what book should I read for', 'search books on', or any book discovery intent."
---

# Book Search — Aibrary

Find the right books for any scenario, need, or question. Powered by Aibrary's AI Librarian methodology.

## Input

The user provides one or more of the following:
- **Search keywords** — specific topics or subjects (e.g., "distributed systems", "leadership")
- **Scenario description** — a situation or challenge they face (e.g., "I'm transitioning from engineer to manager")
- **Question** — a question they want answered through books (e.g., "How do I build better habits?")

## Workflow

1. **Understand intent**: Analyze the user's input to identify the core need — what knowledge gap are they trying to fill? What problem are they trying to solve?

2. **Categorize the search**: Determine the domain(s) involved:
   - Technology & Engineering
   - Business & Management
   - Personal Development & Psychology
   - Science & Research
   - Creative & Design
   - Philosophy & Critical Thinking
   - Health & Wellness
   - Finance & Economics

3. **Match books**: Identify 5-8 books that best match the user's need. Prioritize:
   - **Relevance**: How directly the book addresses the user's specific scenario
   - **Authority**: Well-regarded books by recognized experts
   - **Accessibility**: Appropriate difficulty level for the user's context
   - **Recency**: Prefer recent editions when the field evolves quickly

4. **Rank results**: Order books by relevance to the user's specific need, not by general popularity.

5. **Respond in the user's language**: Detect the language of the user's input and respond in the same language.

## Output Format

For each book, provide:

```
### [Rank]. [Book Title]
**Author**: [Author Name]
**Published**: [Year]
**Why this matches**: [1-2 sentences explaining why this book is relevant to the user's specific scenario/need]
**Core insight**: [The single most important takeaway from the book]
**Best for**: [Who benefits most from this book — experience level, role, situation]
```

### Example Output

**User input**: "I'm leading a team building microservices and we keep running into coordination problems"

---

### 1. Building Microservices (2nd Edition)
**Author**: Sam Newman
**Published**: 2021
**Why this matches**: Directly addresses the coordination challenges that emerge when teams adopt microservices, with practical patterns for service boundaries and team organization.
**Core insight**: Good microservice boundaries follow team boundaries — get the organizational design right and the technical coordination problems reduce dramatically.
**Best for**: Tech leads and architects actively working with microservices who need practical, battle-tested patterns.

### 2. Team Topologies
**Author**: Matthew Skelton & Manuel Pais
**Published**: 2019
**Why this matches**: Your coordination problems may be rooted in team structure rather than technology. This book provides a framework for organizing teams around software architecture.
**Core insight**: Four fundamental team types (stream-aligned, enabling, complicated-subsystem, platform) with three interaction modes can solve most coordination problems.
**Best for**: Engineering leaders redesigning team structures to match their architecture.

---

## Guidelines

- Always explain **why** each book matches the user's specific situation, not just what the book is about
- If the user's need spans multiple domains, include books from different categories
- Include a mix of foundational classics and recent publications
- If a book has been superseded by a newer edition, recommend the latest one
- When the search is vague, ask a clarifying question before listing books
