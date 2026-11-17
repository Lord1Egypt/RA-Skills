---
name: dexio-wiki-setup
description: "Start a new LLM wiki or bring an existing folder of notes or Obsidian vault under maintenance: write the SCHEMA page that tells every agent the wiki's domain, folder layout, page types, frontmatter, tags and thresholds, and point each agent's instructions file at it. Use when creating a knowledge base that agents will maintain, when a wiki has no schema page, or when agents keep writing pages in inconsistent shapes."
license: MIT
metadata:
  author: dexio
  version: "1.2.0"
---

# Set up a wiki

Karpathy's pattern has three layers: immutable raw sources, the wiki the model maintains, and
a schema that tells the model how. The schema is the one agents most often skip, and it is
the one that keeps a wiki consistent once more than a few dozen pages or more than one writer
are involved.

## New wiki

1. **Pick the home.** A folder (in git, so there is history) for one person on one machine.
   A hosted wiki with an MCP server when agents on several machines, or several people, need
   the same pages.
2. **Write `SCHEMA.md`** from `assets/SCHEMA.template.md` in this skill's folder. Fill in:
   - Domain: what the wiki is for, and what it is explicitly not (not a transcript store,
     not the system of record for live data).
   - Layout: folders by kind of page, for example `concepts/`, `entities/`, `people/`,
     `decisions/`, `procedures/`, `queries/`, `raw/`, `_archive/`.
   - Frontmatter: the fields every page carries. Keep `description:` mandatory; it is what
     makes the page list a usable catalog.
   - Tags: a short approved list. Agents add a tag to the schema before using it.
   - Thresholds: when a subject gets its own page, when a page should be split (about 200
     lines), and what never goes in (secrets, routine progress, raw chat).
   - Update policy for conflicts, and who to escalate to.
   - Owner and decision-makers: who gets review digests and escalations, and whose word
     makes something a decision. Review and capture look for these lines.
   - Trust labels: the bracketed labels agents put after a claim. The template's three
     (`(vendor-sourced)`, `(estimate)`, `(unverified)`) are what the other skills use.
3. **Write `README.md`**: two paragraphs on what is where, for a person opening the folder.
4. **Point every agent at the schema.** In `AGENTS.md`, `CLAUDE.md`, or the agent's system
   instructions:

   ```markdown
   ## Wiki
   The team wiki is at <path or URL>. Before substantial work, read its SCHEMA page and
   search it for the topic. Record durable decisions and findings on the page that covers
   them, following the wiki-* skills. Never put secrets in it.
   ```

5. **Ignore run state.** In a git-backed wiki, add `.wiki-state.json` to `.gitignore`;
   `wiki-capture` and `wiki-review` keep their progress there.
6. **Skip the hand-kept index and log** if you have search and history (git, or a hosted
   wiki). Use `description:` fields plus a generated catalog instead
   (`wiki_lint.py --catalog` from the `wiki-lint` skill). A hand-edited `index.md` is fine
   for one writer and under about a hundred pages; past that it drifts, and with several
   writers it is where every change collides.
7. **Seed a few real pages** from real sources (`wiki-ingest`) rather than creating empty
   placeholders for every folder.

## Existing folder of notes or Obsidian vault

1. Run `wiki-lint` to see what is there: pages, links, broken links, pages with no
   frontmatter.
   If the folder is not in git, put it in git first (`git init`, one commit of the current
   state). The other skills lean on history for change notes, recent changes and review.
2. Write the schema to match the best of the existing structure rather than an ideal one;
   moving hundreds of pages at once is a refactor with its own risks (`wiki-refactor`).
3. Add frontmatter and descriptions in batches, starting with the most linked pages.
4. Fix broken links next. Leave orphans and long pages for later passes.

## Pitfalls

- A schema so long agents skim it. Two screens is plenty; put detail in procedure pages.
- Folder by source or by date instead of by subject. Readers look things up by subject.
- Tags invented per page. Ten approved tags beat two hundred ad hoc ones.
- Treating the schema as fixed. When agents keep making the same mistake, the fix usually
  belongs in the schema; change it and say why in the note.
