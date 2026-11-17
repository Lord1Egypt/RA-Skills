---
name: dexio-wiki-orient
description: "Read an LLM wiki before working in it or answering from it: the schema page, the catalog of page descriptions, recent changes, then a targeted search and the canonical page for the topic. Use at the start of any task that will read or change a shared markdown wiki, and before asking a person to repeat context the wiki may already hold."
license: MIT
metadata:
  author: dexio
  version: "1.1.0"
---

# Orient in a wiki

Most wiki damage comes from writing before reading: a duplicate page because the agent did
not search, a convention broken because it did not read the schema, a fact overwritten
because it did not see that another agent changed the page an hour ago. Orienting costs a few
tool calls and prevents all three.

Do this once per task, not once per edit. Do not read the whole wiki.

## Steps

1. **Read the schema.** `SCHEMA.md` (or `AGENTS.md`, `CLAUDE.md`, or the page the wiki's
   README points to). It says where pages go, what frontmatter they carry, which tags exist,
   and when to create a page instead of editing one. The wiki's own schema overrides the
   defaults in these skills.
2. **Scan the catalog.** Folder wiki: list the files, or run
   `python3 <wiki-lint skill>/scripts/wiki_lint.py <wiki> --catalog` to get every page with
   its one-line description. Hosted wiki over MCP: `list_pages`. You are looking for which
   folders exist and which pages sound like your topic, not reading them.
3. **Check recent changes.** Folder in git: `git log --since="7 days ago" --stat -- <wiki>`.
   Hosted: the history tool without a path (on Dexio, `page_history`). Plain folder with no
   history: the most recently modified files (`find <wiki> -name '*.md' -mtime -7`). This
   shows what other agents are working on, so you do not redo or undo it.
4. **Search the topic.** Two or three phrasings: the entity's name, the concept, and the words
   a person would use. Folder: `grep -ril` or ripgrep across the wiki. Hosted: `search_pages`.
   Search before concluding that something is not in the wiki.
5. **Read the canonical page, then its neighbors.** The page that owns the topic, and the one
   or two pages it links to that bear on your task. Stop there unless the task needs more.

## What to carry forward

- The path of the page that owns your topic. If none exists, note that too; `wiki-record`
  decides whether one should.
- The page's `updated` date and, on a hosted wiki, its version, so a later write can detect
  that someone else changed it in between.
- Any claim you will rely on that is about a live system (a price, a config value, an
  account's state, a person's current role). The wiki records what was true when written.
  Check the original source before acting on it.

## Pitfalls

- Treating the wiki as the system of record. It is curated memory. For anything mutable, it
  tells you where to look and what was true then.
- Reading a hand-kept `index.md` instead of listing pages. Index files drift; the file listing
  or the host's page list does not.
- Loading every page "for context". It wastes the budget you need for the task and makes you
  more likely to repeat stale claims.
- Asking a person for context before searching. If the wiki holds it and you ask anyway, you
  have made the wiki pointless for them.
