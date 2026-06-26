---
name: book-deep-reader
description: |
  Deep-read a book and produce teaching-quality notes with critical evaluation and action guidance. Use when: (1) user wants to quickly learn and understand a book's knowledge system, (2) user needs accurate extraction of a book's core ideas to teach others, (3) user provides book title/author/ISBN and asks for a structured reading guide or summary, (4) user wants to verify their understanding of a book against original sources, (5) user wants critical evaluation of a book's value and limitations, (6) user wants cross-disciplinary insights and actionable takeaways. Supports Chinese and English books. Outputs a comprehensive .md file with knowledge framework, chapter details, core principles, practical cases, teaching materials, AND critical evaluation with action plans.
---

# Book Deep Reader

Produce teaching-quality book notes: accurate on the original, structured for quick learning, detailed enough to explain to others.

## Workflow

### Phase 1: Identify the Book

Given a book (title, author, ISBN, or URL), gather foundational info:

1. **Search for the book** using `mimo_web_search` — find Douban/Goodreads pages, publisher descriptions, table of contents, reviews
2. **Fetch key pages** using `web_fetch` — Douban book page (ISBN lookup), publisher pages, review articles
3. **Identify**: book structure (chapters), core framework/model, key cases, author's background
4. **For companion/sequel books**: also fetch the original book's wiki/summary to cross-reference (e.g., *Reinventing Organizations* Wiki for the practice guide)
5. **Identify the book's central question**: What problem is the author trying to solve? Why does it matter?

### Phase 2: Deep Research

Gather rich source material from authoritative references:

1. **Official wiki/community sites** (if they exist) — e.g., reinventingorganizationswiki.com
2. **Detailed reviews and analysis articles** — not just "good book!" but substantive breakdowns
3. **Author's talks/interviews** — YouTube transcripts, keynote summaries
4. **Case study databases** — for books with organizational/practice cases
5. **Academic context research** — what predecessors have done on this topic
6. **Comparative analysis** — other books on the same topic with different viewpoints
7. **Critical reviews** — challenges, limitations, controversies

Search strategy (use `mimo_web_search`):
- `"<book title>" 目录 章节 内容` (for Chinese books)
- `"<English title>" summary chapters key concepts`
- `"author name" "<key concept>" detailed explanation`
- `site:douban.com <ISBN>` or `site:goodreads.com <title>`
- `"<book title>" 批评 局限性 争议` (for critical reviews)
- `"<book title>" 对比 同类书籍 不同观点` (for comparative analysis)
- `"<topic>" 研究进展 前人研究 学术脉络` (for academic context)

Fetch at least 5-8 authoritative sources. Prioritize:
- Table of contents and chapter structure
- The book's own conceptual framework (models, diagrams, key distinctions)
- Detailed case studies with data
- Author's direct quotes and key formulations
- Academic positioning and predecessor research
- Critical reviews and challenges
- Comparative analysis with similar books

### Phase 3: Knowledge Extraction (5-Layer Analysis)

Extract knowledge through 5 layers, from surface to depth:

**Layer 1 — Structure**: What is the book's architecture?
- Chapter outline with one-line purpose per chapter
- How chapters connect (sequential? parallel? recursive?)
- Visual map of the book's flow

**Layer 2 — Core Framework**: What is the book's central model/theory?
- The 1-3 core concepts that everything else builds on
- Key distinctions the author makes (e.g., X vs. Y)
- The "before and after" transformation the book describes

**Layer 3 — Chapter Details**: What does each chapter teach?
- Core question the chapter answers
- Key knowledge points (3-7 per chapter)
- Practical cases with concrete data
- Actionable insights ("how to do this")

**Layer 4 — Depth Mechanisms**: Why do these ideas work?
- Underlying assumptions (what must be true for this to work)
- Causal logic (A leads to B because...)
- Counter-arguments and how the author addresses them
- Limitations and boundary conditions

**Layer 5 — Teaching Materials**: How to explain this to someone else?
- Core quotes / memorable formulations
- Analogies and metaphors the author uses
- Data/evidence for responding to skepticism
- Common misunderstandings and corrections

### Phase 4: Cross-Reference and Verify

Before writing the final output:

1. **Cross-check with original sources**: Every claim must trace back to an authoritative source (the book itself, the author's wiki, verified reviews)
2. **Flag uncertainty**: If a detail cannot be verified, note it as "based on secondary sources" or omit it
3. **Check for omissions**: Compare against the table of contents — are all chapters covered?
4. **Check for consistency**: Do the chapter-level details support the overall framework? Are there contradictions?

### Phase 5: Generate Output

Write the output as a `.md` file in the workspace. Follow the structure in `references/output-template.md`.

Key quality standards:

- **Accuracy over creativity**: Never invent content. If unsure, search again or state the limitation
- **Specific over general**: Include concrete examples, numbers, names, quotes — not just abstract descriptions
- **Structured for skimming AND deep reading**: Headers, tables, and visual maps for quick scanning; detailed prose for deep understanding
- **Teaching-ready**: Someone should be able to read this file and explain the book to others without having read the book itself

## Phase 6: Critical Evaluation (New)

After completing the 5-layer knowledge extraction, conduct a critical evaluation:

**1. Core Question Identification**
- What is the author's central question/problem?
- Why is this question important?

**2. Academic Context Positioning**
- What have predecessors achieved on this question?
- Where does this book fit in the academic conversation?

**3. Innovation Assessment**
- What unique, new answers does the author provide?
- What new evidence, cases, or data support these answers?

**4. Comparative Analysis**
- What different viewpoints exist from contemporary books on the same topic?
- How does this book's approach differ?

**5. Critical Review**
- Has the book's conclusions been challenged?
- What are its limitations and boundary conditions?

**6. Future Directions**
- What new problems and directions does the author propose?
- What remains unresolved?

**7. Cross-disciplinary Insights**
- What启发 can practitioners from other fields draw?
- How can these ideas be applied outside the book's domain?

**8. Most Inspiring Story/Case**
- Which single story or case is most memorable and impactful?
- Why does it resonate?

**9. Actionable Takeaway**
- What is ONE action the reader should take after reading?
- How to implement it immediately?

## Output File

Save to workspace as `<book-short-name>-读书笔记.md` (Chinese) or `<book-short-name>-notes.md` (English).

## Quality Checklist

Before finalizing, verify:

- [ ] All chapters covered with key points
- [ ] Core framework/model clearly articulated
- [ ] At least 3 detailed case studies with data
- [ ] Author's key quotes included
- [ ] Common misconceptions addressed
- [ ] Practical "how to start" guidance included
- [ ] Sources cited (wiki, reviews, publisher pages)
- [ ] No invented or unverified content
- [ ] Can be used to teach the book without reading it
- [ ] **Critical evaluation section completed** (all 9 questions answered)
- [ ] **Actionable takeaway identified** with implementation steps
- [ ] **Cross-disciplinary insights** clearly articulated
