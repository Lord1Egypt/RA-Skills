---
name: dexio-wiki-refactor
description: "Restructure an LLM wiki without breaking it: split oversized pages into focused linked pages, merge duplicate pages, rename or move pages, and archive superseded ones, rewriting every inbound link and confirming zero broken links afterwards. Use when a page passes about 200 lines, when two pages cover the same topic, when the folder layout changes, or when a page is superseded."
license: MIT
metadata:
  author: dexio
  version: "1.0.0"
---

# Refactor a wiki

Agent-kept wikis grow by accretion. Without periodic restructuring, one page absorbs a whole
subject, near-duplicates multiply under slightly different names, and superseded pages keep
getting cited. Refactoring fixes that; done carelessly it is also the fastest way to break
a hundred links at once.

Rule for every operation below: find inbound links first, change them in the same change,
and run `wiki-lint` afterwards. Zero broken links, or the refactor is not done.

Finding inbound links. Folder wiki:
`python3 <wiki-lint skill>/scripts/wiki_lint.py <wiki> --links-to <path>`, or search for the
page name in `[[...]]` and `(...md)` links. Hosted wiki: the page's links-in list from
`read_page`; on Dexio, `move_page` rewrites inbound links itself.

## Split a long page

When a page passes about 200 lines, or covers several things a reader wants separately:

1. Read the whole page and list its distinct subtopics.
2. Move each self-contained subtopic to its own page in the right folder, with full
   frontmatter and the relevant sources. Keep the text; do not summarize it away.
3. Leave the original as the overview: a short section per subtopic with a one- or
   two-sentence summary and a link to the new page. Keep the path, so existing links still
   land on the right topic.
4. Retarget inbound links that were clearly about one subtopic (for example
   `[[vendor#Pricing]]`) to the new page.
5. One change for the split, with a note listing the new pages.

## Merge duplicates

When two pages cover one topic:

1. Choose the survivor: the one with more inbound links, the better path, or the better
   sources.
2. Merge the other's unique content into it, with sources. Where they disagree, follow
   `wiki-conflicts` rather than picking silently.
3. Retarget every inbound link to the survivor.
4. Delete the duplicate or move it to `_archive/`. If other tools or people may still use the
   old path, leave a one-line redirect page instead ("Moved to [[survivor]]").

## Rename or move

1. Choose the new path by the schema's naming rule (lowercase, hyphenated, folder by kind).
2. Move the file (`git mv` in a git-backed wiki, so history follows) or call the host's move
   tool.
3. Rewrite inbound links, including relative markdown links whose `../` depth changed.
4. Update the page's own relative links if it changed folder.

## Archive

When a page is fully superseded but its history matters:

1. Move it to `_archive/` with its links rewritten.
2. Add one line at the top: what replaced it and when.
3. Retarget links that should now point at the replacement; leave links in historical
   records (old decisions, old query pages) pointing at the archive.

## Pitfalls

- Refactoring and editing content in one change. Move first, then edit, so a reviewer can
  see that nothing was lost in the move.
- Relative links. Moving a page one folder deeper breaks every `../` link on it and every
  relative link to it. Wikilinks by path or unique name survive moves better.
- Splitting by date ("2026 notes", "2025 notes") instead of by subject. Readers look things
  up by subject.
- Renaming a page other agents are editing right now. Check recent changes first
  (`wiki-orient`) and do structural work when the wiki is quiet.
