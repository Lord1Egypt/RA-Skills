---
name: book-skill-finder
description: >-
  Instantly find nonfiction books with Goodreads ratings, summaries, key concepts, and AI suggestions for enhancing your agent's knowledge files.
  Covers 4 use cases:
  ① Search books — ("find books about habit formation" "search for books on productivity")
  ② Get book details — ("tell me about Atomic Habits" "what are the key concepts in Deep Work")
  ③ Knowledge injection — ("suggest books for my agent's knowledge base" "recommend books to enhance my AI")
  ④ Reading recommendations — ("what should I read next" "similar books to The Lean Startup")
  Trigger when users say: "find a book" "search books" "book recommendation" "what to read"
  or mention: book lookup / book search / nonfiction / Goodreads / Heardly.
version: 1.0.0
license: MIT
tags:
  - books
  - search
  - nonfiction
  - heardskill
---

# book-skill-finder

Local book search. 5904 nonfiction books, no network calls.

## What it does

- Search 5904 books by title or author
- Return book metadata: title, author, rating, summary, link
- Generate markdown suggestions for knowledge base

## Installation

```bash
openclaw skills install book-skill-finder
```

## Usage

```javascript
const FindBookSkill = require('find-book');
const skill = new FindBookSkill();
const result = skill.search('Atomic Habits');
```

## Data

- Source: Heardly database
- Format: Local JSON cache
- Books: 5904 nonfiction titles
- Network: Zero external calls
- Cost: Free
