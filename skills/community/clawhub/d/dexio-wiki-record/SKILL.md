---
name: dexio-wiki-record
description: "File a decision, finding or fact into an LLM wiki the right way: find the page that already covers it, make the smallest edit that records it, keep frontmatter and dates current, link it to its neighbors, cite where it came from, and leave a change note. Use whenever an agent settles something durable that should outlive the conversation, or a person says to put something in the wiki."
license: MIT
metadata:
  author: dexio
  version: "1.2.0"
---

# Record something in a wiki

The wiki is only as good as what goes in and where it lands. Two failures account for most of
the mess in agent-kept wikis: new pages for topics that already have one, and whole-page
rewrites that silently drop what another writer added. Both are avoided by searching first and
editing small.

## Does it belong?

Record it if someone (a person or another agent) will need it again and could not cheaply
rederive it:

- decisions, with the date, who made them and why
- verified facts about the organization, its systems, its customers or its market
- procedures that worked, and the pitfalls found on the way
- synthesized answers that took real research (file those with `wiki-query`)

Leave it out:

- routine progress, TODOs, and status that will be stale in a week
- raw transcripts or chat logs (keep a source under `raw/` via `wiki-ingest` if it matters)
- commit hashes, PR numbers, and other details the code host already records
- secrets of any kind: tokens, keys, passwords, connection strings, payment details
  (`wiki-lint` flags credential-shaped strings; write where a credential lives, never the
  value)
- anything private a person has not said is fine to share with everyone who reads the wiki

## Steps

1. **Search for the owning page** (`wiki-orient`, step 4). One topic, one page. If a page
   covers the topic, you are editing it, even if you would have organized it differently.
2. **Create a page only past the threshold.** A new page is justified when the subject is
   likely to matter again, appears in several sources, or is central to one authoritative
   source. A passing mention goes on the page that mentions it. Put the page in the folder
   the schema assigns to its kind, with a lowercase hyphenated file name.
3. **Make the smallest edit that records it.** Change the section that is wrong or add a line
   to the section it belongs in. Rewrite a whole page only when you created it in this task
   or the page is being deliberately restructured (`wiki-refactor`).
4. **Write the claim so it survives.**
   - Date anything that can change: "Team plan is $10 a member (pricing page, read
     2026-09-28)", not "Team plan is $10".
   - Say where it came from: a source URL, a raw file, a person and date, or the page it was
     derived from. Put the source next to the claim if the page has several sources.
   - Label trust when it is not first-hand, with the schema's labels in brackets after the
     claim: `(vendor-sourced)` for a company's claim about itself, `(estimate)` for derived
     figures, `(unverified)` for anything recalled, unconfirmed or unsourced, with the reason
     after a colon when it helps (`(unverified: from one chat, not checked)`).
   - For a decision: what was decided, when, by whom, the reason, and what it replaced.
5. **Update the frontmatter.** Bump `updated`. Add the source to `sources`. Make sure
   `description` still says what the page holds after your change. New pages get the full
   frontmatter the schema asks for; the default is:

   ```yaml
   ---
   title: Page Title
   description: One line on what the page answers or holds.
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   type: entity | concept | comparison | procedure | decision | query | summary
   tags: [from-the-schema-taxonomy]
   sources: [where the content came from]
   ---
   ```
6. **Link it.** Link the new content to the pages it depends on, and link to it from the one
   or two pages a reader would come from. Aim for at least two useful links on a new page.
   If you mention another page's subject by name, make it a link.
7. **Leave a change note.** Git: a commit message saying what changed and why, one change per
   commit. Hosted wiki: the `note` field on the write, with your agent name. "Add Q3 pricing
   from vendor page; replaces August figure" is a note. "Update page" is not. A plain folder
   has no history: there the dates and sources in the text are the record, so keep a dated
   line of anything you replace, and suggest putting the wiki in git.
8. **Tell the person what you recorded and where**, by path, in one line.

## Conflicts

If what you are recording contradicts the page, do not overwrite it. Follow `wiki-conflicts`:
check dates and provenance, keep both claims if it is unresolved, and flag it.

## Pitfalls

- Appending a new dated section to the bottom of a page every time. The page becomes a log
  and the current answer is buried. Update the section the fact belongs in; history keeps the
  old version.
- Recording your own inference as a finding. Mark it as your read ("likely", "our estimate")
  and give the evidence it rests on.
- Several lists agreeing is not corroboration when they were drawn from the same place. Name
  what a source could and could not have seen before quoting a rate from it.
- Writing for yourself. Write for an agent that has never seen this conversation.
