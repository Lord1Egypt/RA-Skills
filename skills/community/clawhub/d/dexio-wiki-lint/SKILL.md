---
name: dexio-wiki-lint
description: "Check an LLM wiki's health and fix what it finds: broken links, leaked credentials, orphaned and unreferenced pages, missing frontmatter or descriptions, stale pages, oversized pages and duplicate titles. Ships a zero-dependency Python checker for markdown folders ([[wikilinks]] and relative links, Obsidian-compatible). Use on a schedule, before committing or merging wiki changes, after a refactor, or when an agent reports it cannot find a page."
license: MIT
metadata:
  author: dexio
  version: "1.2.0"
---

# Lint a wiki

A wiki kept by agents decays in predictable ways: links point at pages that were renamed or
never written, new pages nobody links to, summaries that fall behind the pages they summarize,
and pages that grow until nobody reads them. Linting finds these mechanically so the fixing
can be deliberate.

Two findings are defects: a broken link and a credential-shaped string. Everything else in
the report is information that needs a judgment call, not an automatic fix.

## Run the check

Markdown folder (Obsidian vault, git repo, any directory of `.md` files):

```bash
python3 scripts/wiki_lint.py path/to/wiki            # readable report
python3 scripts/wiki_lint.py path/to/wiki --json     # for you to parse
```

`scripts/` is inside this skill's folder. Python 3.8 or later, no packages. Options:
`--stale-days 90`, `--max-lines 200`, `--strict` (also fail on frontmatter problems),
`--today 2026-09-28` (measure ages from that date instead of the system clock).

Hosted wiki over MCP: call the host's health tool instead (on Dexio, `wiki_health`). It
reports the same categories.

Exit status 1 means at least one broken link or possible secret, so the same command works as
a pre-commit hook or a CI step.

## Fix in this order

1. **Secrets.** The report shows where and what kind, never the value. Remove the value from
   the page at once, replace it with where the credential lives ("in the deploy host's
   `.env`"), and tell a person: the value is still in history, so the credential has to be
   rotated. A placeholder or an example key the checker flags can be reworded so it no longer
   looks like one.
2. **Broken links.** For each, decide which is true:
   - The page was renamed or moved: point the link at the new path.
   - The page should exist: it appears in `wanted`, ranked by how many pages link to it. A
     target wanted by three or more pages usually deserves a real page; write it with
     `wiki-record`.
   - The link was speculative: remove the brackets and keep the words.
   Never create an empty stub just to clear the error. A stub is a broken link that no longer
   shows up.
3. **Frontmatter.** Add the missing `description` (one line saying what the page answers or
   holds, not the question that started it), `title`, or a valid `updated` date. The
   description is what makes the catalog useful, so write it for someone deciding whether to
   open the page.
4. **Orphaned pages** (no links in or out). Read the page. If it still matters, link it from
   the one or two pages a reader would come from and link out from it to its neighbors. If it
   is superseded, archive it (`wiki-refactor`). If it is a passing mention, fold its content
   into the page that covers the topic and archive it.
5. **Unreferenced pages** (links out, none in). Same as orphans, lower priority: search finds
   them, browsing does not.
6. **Stale pages.** "Unchanged for N days while pages it links to changed" is a hint, not a
   verdict. Reread the page against the newer pages and the original sources. If it still
   holds, bump `updated` and say in the change note that you rechecked it. If not, fix it or
   record the conflict (`wiki-conflicts`). A page past its own `stale_after` date must be
   rechecked before anyone relies on it.
7. **Long pages.** Split past about 200 lines (`wiki-refactor`). Long pages are where
   contradictions hide, because nobody rereads the whole thing before appending.
8. **Duplicate titles.** Two pages with one title usually means two pages on one topic.
   Merge them (`wiki-refactor`), or retitle one so each title says what is different.

Then run the check again and confirm zero broken links and zero secrets before you finish.

## Other uses of the script

```bash
python3 scripts/wiki_lint.py path/to/wiki --catalog          # every page and its description
python3 scripts/wiki_lint.py path/to/wiki --links-to concepts/llm-wiki   # before a rename
python3 scripts/wiki_lint.py path/to/wiki --verify-queue 10  # what to fact-check next
```

`--catalog` prints the catalog from page descriptions, grouped by folder. Generate it when
you need an index instead of keeping `index.md` by hand, which drifts out of sync and is the
file every parallel writer collides on. `--verify-queue` ranks pages for `wiki-verify`.

## Automate it

Pre-commit hook in a git-backed wiki (`.git/hooks/pre-commit`, made executable):

```bash
#!/bin/sh
python3 path/to/wiki_lint.py . >/dev/null || { python3 path/to/wiki_lint.py .; exit 1; }
```

GitHub Actions:

```yaml
- uses: actions/checkout@v4
- run: python3 skills/wiki-lint/scripts/wiki_lint.py wiki
```

A scheduled agent run is better than either for the judgment calls: run the check weekly,
fix broken links and frontmatter, and report orphans, stale pages and long pages to a person
rather than deleting anything.

## Pitfalls

- Do not fix a broken link by deleting the sentence around it. The sentence is usually right;
  only the target is wrong.
- Do not bump `updated` on a stale page without rereading it. That turns a warning into a
  false claim that the page was checked.
- Do not batch hundreds of fixes into one change. Group by kind (all link fixes, then all
  descriptions) so a reviewer can read the diff and a bad fix is easy to revert.
- Resolution rules differ between tools. This checker resolves the exact path from the wiki
  root, then the path relative to the linking page, then the one page with that file name.
  If your viewer resolves differently, trust your viewer and report the mismatch.
