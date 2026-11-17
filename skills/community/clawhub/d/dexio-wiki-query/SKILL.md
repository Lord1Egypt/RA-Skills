---
name: dexio-wiki-query
description: "Answer a question from an LLM wiki: find and read the relevant pages, answer with the page paths you relied on, check anything mutable at its original source, say plainly what the wiki does not cover, and file substantial answers back as query pages so the research compounds. Use when a person asks something the wiki may cover, or after an answer took real research."
license: MIT
metadata:
  author: dexio
  version: "1.0.0"
---

# Answer from a wiki

A wiki earns its upkeep when answers come from it faster and better than from scratch, and
when good answers are kept so the next question starts further ahead.

## Steps

1. **Orient on the question** (`wiki-orient`): search two or three phrasings, read the
   canonical page and the neighbors that bear on it.
2. **Answer from what you read, and cite it.** Give the page paths the answer rests on. If
   you combine pages, say so. If a page's claim carries a trust label (vendor-sourced,
   estimate, unverified), carry the label into the answer.
3. **Check mutable facts at their source** before presenting them as current: prices,
   configuration, account state, who holds a role, anything with a date older than the
   decision it will feed. Say what you checked. If the source disagrees with the wiki, the
   answer uses the source and the wiki gets fixed (`wiki-record` or `wiki-conflicts`).
4. **Say what the wiki does not cover.** "The wiki has nothing on X" is a useful answer; a
   plausible guess presented as if it came from the wiki is a harmful one. If you fill the
   gap from outside research, mark which parts came from where.
5. **File the answer back when it is substantial.** If the answer needed several pages,
   outside research, or a judgment worth keeping, write it as a query page (below). Trivial
   lookups are not filed.
6. **Fix what you found on the way.** A broken link, a stale date, a missing link between two
   pages you needed together: fix it with a small edit and a note, or report it.

## Query page

Under `queries/` (or where the schema puts them), named for the question:

```markdown
---
title: Which vendors include SSO on their base plan?
description: One line with the short answer, not the question.
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: query
tags: [...]
sources: [pages and URLs consulted]
confidence: high | medium | low
---

# Which vendors include SSO on their base plan?

Question (who asked, date).

## Short answer
Two to four sentences.

## Evidence
What was consulted, with links to wiki pages and sources, and the numbers that carry the
answer.

## Confidence and gaps
What would change the answer, and what was not checked.
```

Link the query page from the pages it draws on when it adds something they lack, so the
answer is found from the topic and not only by search. When a follow-up question arrives in
the same thread, add it as a section of the same query page rather than a new page.

## Pitfalls

- Answering from memory with the wiki open. If you did not read it in the wiki or a source
  this session, it is unverified; say so.
- Citing a page for a claim the page does not make. Quote or paraphrase closely enough that
  the reader can find the sentence.
- Filing every answer. A `queries/` folder full of one-line lookups buries the real
  syntheses.
