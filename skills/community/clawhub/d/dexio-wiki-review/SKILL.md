---
name: dexio-wiki-review
description: "Review what agents recently wrote to an LLM wiki: read each change as a diff, accept, fix or revert it with a note, promote drafts that pass, and send a person a short digest of what changed and what needs their call. Use daily or weekly on a wiki that agents write to, when drafts are waiting for approval, or after a burst of agent writes such as a large ingest."
license: MIT
metadata:
  author: dexio
  version: "1.1.0"
---

# Review agent edits

When agents write to a wiki unsupervised, most edits are fine and a few are quietly harmful:
a rewrite that dropped another writer's section, a guess filed as a decision, a secret, a
claim with no source. Nobody notices until someone relies on it. Review is the step that
catches them while they are one change old and easy to undo.

The reviewer should not be the agent that made the change. If it has to be, say so in the
digest.

## Steps

1. **List changes since the last review.** Git: `git log <last reviewed commit>..HEAD --stat
   --format='%h %an %ad %s' -- <wiki>`. Hosted wiki: the change history without a path (on
   Dexio, `page_history`), which gives the writer, the note and the version. With no earlier
   review, take the last seven days (`git log --since="7 days ago"`). Skip your own earlier
   review commits; the digest that made them already listed them.

   Keep the state in `.wiki-state.json` at the wiki root, listed in `.gitignore`:
   `{"review": {"last_commit": "<hash>", "last_time": "<ISO time>", "open": ["<item>"]}}`.
   On a hosted wiki keep it in the agent's own workspace, with the last version or time.
2. **Read each change as a diff, not the whole page.** Git: `git show <commit> -- <page>`.
   Hosted: compare the version before and after (on Dexio, `read_page` with `revision`).
3. **Check it** against these, in order:
   - Secrets or private details (`wiki-lint` flags credential-shaped strings).
   - Lost content: removed lines that nobody replaced. Whole-page rewrites are the usual
     cause.
   - Right page: the change belongs on the page that owns the topic, not a new duplicate.
   - Provenance: dated, sourced, and labelled with the schema's trust labels
     (`(vendor-sourced)`, `(estimate)`, `(unverified)` by default).
   - Decisions: something recorded as decided was decided by someone with the authority,
     not proposed by an agent.
   - Conflicts: the change contradicts another page without saying so (`wiki-conflicts`).
   - Structure: run `wiki-lint`; the change broke no links and left frontmatter valid.
   - The note says what changed and why.
4. **Act on each change.** Accept it, fix it with a small follow-up edit, or revert it
   (`git revert` of that commit, or restore the earlier version on a hosted wiki), always
   with a note saying why. By finding:
   - Secret: remove it now. Replace the value with where the credential lives, or revert if
     adding it was all the commit did. History still holds the value, so escalate: the
     credential has to be rotated.
   - Lost content: restore it (fix).
   - Decision recorded without someone with authority deciding it: revert it, or relabel it
     as a proposal, and escalate asking who decided. Never leave it standing as a decision
     while you wait.
   - Missing source or label: label the claim `(unverified)`; escalate if something relies
     on it.
   - Wrong page or duplicate: move the content to the page that owns the topic.
   - Unmarked contradiction: `wiki-conflicts`.
   - Anything else that needs a person's judgment: escalate, and leave the change in place
     only if it does no harm while it waits.

   Revert the one bad change, not the batch around it. If later commits build on it and a
   revert would conflict, fix forward instead and say so.
5. **Promote drafts.** Pages marked `status: draft` or kept under `drafts/` that pass the
   checks move to their real folder (`wiki-refactor`, move) or lose the draft flag. Drafts
   that fail get a note on what is missing. A draft whose kind has no folder in the schema
   stays a draft; ask where it goes.
6. **Send a digest** to the wiki's owner (the schema's `Owner:` line; if none, whoever asked
   for the review), in chat or email, not as a wiki page: how many changes and by whom,
   what you fixed or reverted and why, your own review commits so they can be checked,
   drafts promoted, and a short list of what needs their call. Five to fifteen lines. With
   no channel, return it as the run's result. Skip it when nothing happened.
7. **Update the state file** with the last commit or version you reviewed and the items
   still open.

## Cadence

Daily for a wiki that several agents write to every day; weekly otherwise; right after any
large ingest or migration. A review that waits a month turns into an audit.

## Pitfalls

- Reviewing the change notes instead of the diffs. Notes say what the writer meant to do.
- Rubber-stamping. If every change is accepted for weeks, check whether you are reading the
  diffs.
- Reverting a whole day's batch for one bad edit.
- Filing the digest in the wiki. It is routine progress; the history already records it.
